from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from risksignal.adapters.data_governance.mapper import CanonicalProjection, project
from risksignal.adapters.data_governance.repository import load_governance, persist_governance
from risksignal.canonical.models import (
    Decision,
    Evidence,
    Investigation,
    Pattern,
    Recommendation,
    Signal,
)
from risksignal.intelligence.context import Context, ContextEngine
from risksignal.intelligence.evidence import EvidenceEngine
from risksignal.intelligence.investigation import InvestigationBuilder
from risksignal.intelligence.pattern import PatternEngine
from risksignal.intelligence.recommendation import RecommendationBuilder
from risksignal.intelligence.signal import SignalEngine
from risksignal.persistence.duckdb_store import DuckDBStore


@dataclass
class PipelineResult:
    context: Context
    patterns: list[Pattern]
    signals: list[Signal]
    evidence: list[Evidence]
    investigations: list[Investigation]
    recommendations: list[Recommendation]
    decisions: list[Decision] = field(default_factory=list)


def ingest_data_governance(store: DuckDBStore, seed: dict[str, list]) -> CanonicalProjection:
    persist_governance(store, seed)
    loaded = load_governance(store)
    projection = project(**loaded)
    store.replace_canonical(
        entities=projection.entities,
        relationships=projection.relationships,
        observations=projection.observations,
        events=projection.events,
    )
    return projection


def run_intelligence(
    store: DuckDBStore,
    *,
    subject_entity_id: str,
    as_of: datetime,
    detected_at: datetime | None = None,
    required_relationship_type: str = "owner",
) -> PipelineResult:
    clock = detected_at or as_of
    entities = store.load_entities()
    subject = next(item for item in entities if item.entity_id == subject_entity_id)
    context = ContextEngine().build(
        subject=subject,
        relationships=store.load_relationships(),
        observations=store.load_observations(),
        events=store.load_events(),
        as_of=as_of,
    )
    patterns = PatternEngine(
        required_relationship_type=required_relationship_type
    ).detect(context, detected_at=clock)
    signals = SignalEngine().emit(context=context, patterns=patterns, detected_at=clock)

    evidence_items: list[Evidence] = []
    investigations: list[Investigation] = []
    recommendations: list[Recommendation] = []
    pattern_by_id = {item.pattern_id: item for item in patterns}

    for pattern in patterns:
        store.save_pattern(pattern)
    for signal in signals:
        store.save_signal(signal)
        pattern = pattern_by_id[signal.pattern_id]
        collected = EvidenceEngine().collect(
            signal=signal, pattern=pattern, patterns=patterns, context=context
        )
        store.save_evidence(collected)
        evidence_items.extend(collected)
        investigation = InvestigationBuilder().build(
            signal=signal,
            pattern=pattern,
            evidence=collected,
            context=context,
            created_at=clock,
        )
        store.save_investigation(investigation)
        investigations.append(investigation)
        recommendation = RecommendationBuilder().build(
            investigation_id=investigation.investigation_id,
            signal=signal,
            evidence=collected,
            created_at=clock,
        )
        store.save_recommendation(recommendation)
        recommendations.append(recommendation)

    return PipelineResult(
        context=context,
        patterns=patterns,
        signals=signals,
        evidence=evidence_items,
        investigations=investigations,
        recommendations=recommendations,
    )


def record_decision(
    store: DuckDBStore,
    *,
    recommendation_id: str,
    decided_by: str,
    decision_type: str,
    decided_at: datetime,
    notes: str = "",
) -> Decision:
    decision = Decision(
        decision_id=f"dec:{recommendation_id}",
        recommendation_id=recommendation_id,
        decided_by=decided_by,
        decision_type=decision_type,
        decided_at=decided_at,
        notes=notes,
    )
    store.save_decision(decision)
    return decision
