from __future__ import annotations

from uuid import uuid4

from risksignal.canonical.models import Evidence, Pattern, Relationship, Signal
from risksignal.intelligence.context import Context
from risksignal.intelligence.evidence_roles import CONSTITUTIVE_ROLES


class EvidenceEngine:
    def collect(
        self,
        *,
        signal: Signal,
        pattern: Pattern,
        patterns: list[Pattern],
        context: Context,
    ) -> list[Evidence]:
        return _constitutive(signal, pattern, patterns, context) + _contextual(signal, context)


def _constitutive(
    signal: Signal,
    pattern: Pattern,
    patterns: list[Pattern],
    context: Context,
) -> list[Evidence]:
    if pattern.pattern_type == "compound":
        return _compound_constitutive(signal, pattern, patterns, context)
    return _atomic_constitutive(signal, pattern, context)


def _atomic_constitutive(signal: Signal, pattern: Pattern, context: Context) -> list[Evidence]:
    items = [
        Evidence(
            evidence_id=f"evd:{uuid4()}",
            signal_id=signal.signal_id,
            referenced_object_type="pattern",
            referenced_id=pattern.pattern_id,
            role="detected_pattern",
            description=pattern.pattern_type,
            available_at=pattern.as_of,
        )
    ]
    if pattern.pattern_type == "consecutive_metric_decline":
        observation_ids = set(pattern.attributes.get("observation_ids", []))
        for obs in context.observations:
            if obs.observation_id not in observation_ids:
                continue
            items.append(
                Evidence(
                    evidence_id=f"evd:{uuid4()}",
                    signal_id=signal.signal_id,
                    referenced_object_type="observation",
                    referenced_id=obs.observation_id,
                    role="supporting_observation",
                    description=(
                        f"{obs.metric_name}={obs.value} observed_at={obs.observed_at.isoformat()}"
                    ),
                    available_at=obs.available_at,
                )
            )
    if pattern.pattern_type == "missing_relationship":
        expired_ids = set(pattern.attributes.get("expired_relationship_ids", []))
        expired = [
            rel
            for rel in context.historical_relationships
            if rel.relationship_id in expired_ids
        ]
        for rel in expired:
            items.append(_relationship_evidence(signal, rel, "expired_relationship"))
        if not expired:
            items.append(
                Evidence(
                    evidence_id=f"evd:{uuid4()}",
                    signal_id=signal.signal_id,
                    referenced_object_type="entity",
                    referenced_id=context.subject.entity_id,
                    role="missing_required_relationship",
                    description=(
                        "no active "
                        f"{pattern.attributes.get('required_relationship_type')} "
                        "relationship"
                    ),
                    available_at=context.as_of,
                )
            )
    return items


def _compound_constitutive(
    signal: Signal,
    pattern: Pattern,
    patterns: list[Pattern],
    context: Context,
) -> list[Evidence]:
    items = [
        Evidence(
            evidence_id=f"evd:{uuid4()}",
            signal_id=signal.signal_id,
            referenced_object_type="pattern",
            referenced_id=pattern.pattern_id,
            role="detected_pattern",
            description="compound",
            available_at=pattern.as_of,
        )
    ]
    by_id = {item.pattern_id: item for item in patterns}
    for child_id in pattern.attributes.get("component_pattern_ids", []):
        child = by_id[child_id]
        items.append(
            Evidence(
                evidence_id=f"evd:{uuid4()}",
                signal_id=signal.signal_id,
                referenced_object_type="pattern",
                referenced_id=child.pattern_id,
                role="constituent_pattern",
                description=child.pattern_type,
                available_at=child.as_of,
            )
        )
        for fact in _atomic_constitutive(signal, child, context):
            if fact.role == "detected_pattern":
                continue
            items.append(fact)
    return items


def _contextual(signal: Signal, context: Context) -> list[Evidence]:
    items: list[Evidence] = []
    for event in context.events:
        items.append(
            Evidence(
                evidence_id=f"evd:{uuid4()}",
                signal_id=signal.signal_id,
                referenced_object_type="event",
                referenced_id=event.event_id,
                role="contextual_event",
                description=event.payload.get("description", event.event_type),
                available_at=event.available_at,
            )
        )
    for rel in context.relationships:
        items.append(_relationship_evidence(signal, rel, "context_relationship"))
    return items


def _relationship_evidence(signal: Signal, rel: Relationship, role: str) -> Evidence:
    return Evidence(
        evidence_id=f"evd:{uuid4()}",
        signal_id=signal.signal_id,
        referenced_object_type="relationship",
        referenced_id=rel.relationship_id,
        role=role,
        description=f"{rel.relationship_type} {rel.from_entity_id}->{rel.to_entity_id}",
        available_at=rel.available_at,
    )
