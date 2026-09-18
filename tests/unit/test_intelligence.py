from datetime import datetime, timedelta

from risksignal.canonical.models import Entity, Observation, Relationship
from risksignal.intelligence.context import ContextEngine
from risksignal.intelligence.evidence import CONSTITUTIVE_ROLES, EvidenceEngine
from risksignal.intelligence.pattern import MissingRelationshipDetector, PatternEngine
from risksignal.intelligence.signal import SignalEngine


def _subject(criticality: str = "critical") -> Entity:
    return Entity(
        entity_id="entity:X",
        entity_type="subject",
        name="X",
        source_system="test",
        source_id="X",
        attributes={"criticality": criticality},
    )


def _series(metric_name: str = "timeliness", *, start: int = 90, step: int = 4) -> list[Observation]:
    rows = []
    for day in range(8):
        observed = datetime(2026, 1, 1) + timedelta(days=day)
        rows.append(
            Observation(
                observation_id=f"o-{metric_name}-{day}",
                subject_entity_id="entity:X",
                observation_type="metric",
                metric_name=metric_name,
                value=start - day * step,
                observed_at=observed,
                available_at=observed + timedelta(days=1),
                source_system="test",
                source_id=f"o-{metric_name}-{day}",
            )
        )
    return rows


def _relationship(
    *,
    relationship_id: str,
    relationship_type: str,
    valid_to: datetime | None = None,
    available_at: datetime | None = None,
) -> Relationship:
    start = datetime(2026, 1, 1)
    return Relationship(
        relationship_id=relationship_id,
        from_entity_id="entity:person",
        to_entity_id="entity:X",
        relationship_type=relationship_type,
        available_at=available_at or start,
        source_system="test",
        source_id=relationship_id,
        valid_from=start,
        valid_to=valid_to,
    )


def test_pattern_engine_detects_consecutive_decline():
    as_of = datetime(2026, 1, 10, 12, 0, 0)
    context = ContextEngine().build(
        subject=_subject(),
        relationships=[],
        observations=_series(),
        events=[],
        as_of=as_of,
    )
    patterns = PatternEngine(min_consecutive=5).detect(context, detected_at=as_of)
    assert [item.pattern_type for item in patterns] == ["consecutive_metric_decline"]
    assert patterns[0].attributes["metric_name"] == "timeliness"


def test_context_excludes_observations_not_yet_available():
    as_of = datetime(2026, 1, 5, 9, 0, 0)
    context = ContextEngine().build(
        subject=_subject(),
        relationships=[],
        observations=_series(),
        events=[],
        as_of=as_of,
    )
    assert all(obs.available_at <= as_of for obs in context.observations)
    assert len(context.observations) < 8


def test_signal_requires_critical_subject_for_decline():
    as_of = datetime(2026, 1, 10, 12, 0, 0)
    low = ContextEngine().build(
        subject=_subject("low"),
        relationships=[],
        observations=_series(),
        events=[],
        as_of=as_of,
    )
    patterns = PatternEngine().detect(low, detected_at=as_of)
    signals = SignalEngine().emit(context=low, patterns=patterns, detected_at=as_of)
    assert patterns
    assert signals == []


def test_missing_relationship_when_required_type_absent():
    as_of = datetime(2026, 1, 10, 12, 0, 0)
    context = ContextEngine().build(
        subject=_subject(),
        relationships=[],
        observations=[],
        events=[],
        as_of=as_of,
    )
    patterns = MissingRelationshipDetector("accountable").detect(context, detected_at=as_of)
    assert len(patterns) == 1
    assert patterns[0].pattern_type == "missing_relationship"
    assert patterns[0].attributes["required_relationship_type"] == "accountable"
    assert patterns[0].attributes["active_count"] == 0


def test_expired_relationship_is_missing_and_cited():
    as_of = datetime(2026, 1, 15, 10, 0, 0)
    expired = _relationship(
        relationship_id="rel-expired",
        relationship_type="accountable",
        valid_to=datetime(2026, 1, 10),
    )
    context = ContextEngine().build(
        subject=_subject(),
        relationships=[expired],
        observations=[],
        events=[],
        as_of=as_of,
    )
    assert context.relationships == []
    assert [rel.relationship_id for rel in context.historical_relationships] == ["rel-expired"]
    patterns = PatternEngine(required_relationship_type="accountable").detect(
        context, detected_at=as_of
    )
    missing = next(item for item in patterns if item.pattern_type == "missing_relationship")
    assert "rel-expired" in missing.attributes["expired_relationship_ids"]
    signals = SignalEngine().emit(context=context, patterns=patterns, detected_at=as_of)
    signal = next(item for item in signals if item.signal_type == "missing_relationship")
    evidence = EvidenceEngine().collect(
        signal=signal, pattern=missing, patterns=patterns, context=context
    )
    constitutive = [item for item in evidence if item.role in CONSTITUTIVE_ROLES]
    assert any(item.role == "expired_relationship" for item in constitutive)
    assert all(item.available_at <= as_of for item in evidence)


def test_active_required_relationship_does_not_fire():
    as_of = datetime(2026, 1, 15, 10, 0, 0)
    active = _relationship(relationship_id="rel-active", relationship_type="accountable")
    context = ContextEngine().build(
        subject=_subject(),
        relationships=[active],
        observations=[],
        events=[],
        as_of=as_of,
    )
    patterns = PatternEngine(required_relationship_type="accountable").detect(
        context, detected_at=as_of
    )
    assert all(item.pattern_type != "missing_relationship" for item in patterns)


def test_two_declines_in_same_family_are_not_compound():
    as_of = datetime(2026, 1, 10, 12, 0, 0)
    observations = _series("timeliness") + _series("dq_score", start=88, step=2)
    context = ContextEngine().build(
        subject=_subject(),
        relationships=[],
        observations=observations,
        events=[],
        as_of=as_of,
    )
    patterns = PatternEngine(min_consecutive=5).detect(context, detected_at=as_of)
    types = [item.pattern_type for item in patterns]
    assert types.count("consecutive_metric_decline") == 2
    assert "compound" not in types


def test_compound_combines_independent_indicator_families():
    as_of = datetime(2026, 1, 15, 10, 0, 0)
    expired = _relationship(
        relationship_id="rel-expired",
        relationship_type="accountable",
        valid_to=datetime(2026, 1, 10),
    )
    future = Observation(
        observation_id="o-future",
        subject_entity_id="entity:X",
        observation_type="metric",
        metric_name="timeliness",
        value=1.0,
        observed_at=datetime(2026, 1, 16),
        available_at=datetime(2026, 1, 20, 9, 0, 0),
        source_system="test",
        source_id="o-future",
    )
    context = ContextEngine().build(
        subject=_subject(),
        relationships=[expired],
        observations=_series() + [future],
        events=[],
        as_of=as_of,
    )
    patterns = PatternEngine(
        min_consecutive=5, required_relationship_type="accountable"
    ).detect(context, detected_at=as_of)
    types = {item.pattern_type for item in patterns}
    assert types == {"consecutive_metric_decline", "missing_relationship", "compound"}
    compound = next(item for item in patterns if item.pattern_type == "compound")
    component_types = set(compound.attributes["component_types"])
    assert component_types == {"consecutive_metric_decline", "missing_relationship"}

    signals = SignalEngine().emit(context=context, patterns=patterns, detected_at=as_of)
    compound_signal = next(item for item in signals if item.signal_type == "compound_risk")
    evidence = EvidenceEngine().collect(
        signal=compound_signal, pattern=compound, patterns=patterns, context=context
    )
    constitutive = [item for item in evidence if item.role in CONSTITUTIVE_ROLES]
    assert {item.role for item in constitutive} >= {
        "detected_pattern",
        "constituent_pattern",
        "supporting_observation",
        "expired_relationship",
    }
    assert all(item.available_at <= as_of for item in evidence)
    assert not any("future" in item.referenced_id for item in evidence)
    decline_obs = [
        item
        for item in constitutive
        if item.role == "supporting_observation"
    ]
    assert decline_obs
    assert any(item.role == "constituent_pattern" for item in constitutive)
