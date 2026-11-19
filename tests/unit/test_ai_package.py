from datetime import datetime, timedelta

import pytest

from risksignal.canonical.models import (
    Entity,
    Evidence,
    Observation,
    Pattern,
    Relationship,
    Signal,
)
from risksignal.intelligence.context import ContextEngine
from risksignal.intelligence.evidence import EvidenceEngine
from risksignal.intelligence.pattern import PatternEngine
from risksignal.intelligence.signal import SignalEngine
from risksignal.intelligence.ai.contracts import EvidencePackage
from risksignal.intelligence.ai.package import (
    DeterministicEvidencePackageBuilder,
)

def _subject(criticality: str = "critical") -> Entity:
    return Entity(
        entity_id="entity:X",
        entity_type="subject",
        name="X",
        source_system="test",
        source_id="X",
        attributes={"criticality": criticality},
    )


def _series(
    metric_name: str = "timeliness",
    *,
    start: int = 90,
    step: int = 4,
) -> list[Observation]:
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


def test_evidence_package_contains_closed_deterministic_evidence():
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
        min_consecutive=5,
        required_relationship_type="accountable",
    ).detect(
        context,
        detected_at=as_of,
    )

    signals = SignalEngine().emit(
        context=context,
        patterns=patterns,
        detected_at=as_of,
    )

    compound_pattern = next(
        item for item in patterns if item.pattern_type == "compound"
    )

    compound_signal = next(
        item for item in signals if item.signal_type == "compound_risk"
    )

    evidence = EvidenceEngine().collect(
        signal=compound_signal,
        pattern=compound_pattern,
        patterns=patterns,
        context=context,
    )

    package = DeterministicEvidencePackageBuilder().build(
        subject=_subject(),
        signal=compound_signal,
        pattern=compound_pattern,
        evidence=evidence,
        as_of=as_of,
    )

    assert package.as_of == as_of
    assert package.subject_entity_id == "entity:X"
    assert package.subject_name == "X"

    assert package.signal_id == compound_signal.signal_id
    assert package.signal_type == "compound_risk"
    assert package.signal_severity == compound_signal.severity

    assert package.pattern_id == compound_pattern.pattern_id
    assert package.pattern_type == "compound"

    assert package.constitutive_evidence

    assert all(
        item.available_at <= as_of
        for item in package.constitutive_evidence
    )

    assert all(
        item.available_at <= as_of
        for item in package.contextual_evidence
    )

    all_evidence_ids = {
        item.evidence_id
        for item in package.constitutive_evidence
        + package.contextual_evidence
    }

    deterministic_evidence_ids = {
        item.evidence_id
        for item in evidence
    }

    assert all_evidence_ids == deterministic_evidence_ids

    assert not any(
        "future" in item.referenced_id
        for item in package.constitutive_evidence
        + package.contextual_evidence
    )


def test_evidence_package_preserves_constitutive_and_contextual_roles():
    as_of = datetime(2026, 1, 15, 10, 0, 0)

    expired = _relationship(
        relationship_id="rel-expired",
        relationship_type="accountable",
        valid_to=datetime(2026, 1, 10),
    )
    active_context = _relationship(
        relationship_id="rel-context",
        relationship_type="steward",
    )
    context = ContextEngine().build(
        subject=_subject(),
        relationships=[expired, active_context],
        observations=_series(),
        events=[],
        as_of=as_of,
    )

    patterns = PatternEngine(
        min_consecutive=5,
        required_relationship_type="accountable",
    ).detect(
        context,
        detected_at=as_of,
    )

    signals = SignalEngine().emit(
        context=context,
        patterns=patterns,
        detected_at=as_of,
    )

    compound_pattern = next(
        item for item in patterns if item.pattern_type == "compound"
    )

    compound_signal = next(
        item for item in signals if item.signal_type == "compound_risk"
    )

    evidence = EvidenceEngine().collect(
        signal=compound_signal,
        pattern=compound_pattern,
        patterns=patterns,
        context=context,
    )

    package = DeterministicEvidencePackageBuilder().build(
        subject=_subject(),
        signal=compound_signal,
        pattern=compound_pattern,
        evidence=evidence,
        as_of=as_of,
    )

    constitutive_roles = {
        item.role for item in package.constitutive_evidence
    }

    contextual_roles = {
        item.role for item in package.contextual_evidence
    }

    assert "detected_pattern" in constitutive_roles
    assert "constituent_pattern" in constitutive_roles
    assert "supporting_observation" in constitutive_roles
    assert "expired_relationship" in constitutive_roles

    assert "context_relationship" in contextual_roles

    assert not constitutive_roles.intersection(contextual_roles)


def test_evidence_package_excludes_future_dated_evidence():
    as_of = datetime(2026, 1, 15, 10, 0, 0)
    subject = _subject()

    signal = Signal(
        signal_id="signal:test",
        subject_entity_id=subject.entity_id,
        signal_type="test_signal",
        severity="high",
        detected_at=as_of,
        as_of=as_of,
        pattern_id="pattern:test",
        summary="Test signal",
    )

    pattern = Pattern(
        pattern_id="pattern:test",
        pattern_type="test_pattern",
        subject_entity_id=subject.entity_id,
        detected_at=as_of,
        as_of=as_of,
        window_start=as_of - timedelta(days=7),
        window_end=as_of,
    )

    future_evidence = Evidence(
        evidence_id="evidence:future",
        signal_id=signal.signal_id,
        referenced_object_type="observation",
        referenced_id="observation:future",
        role="supporting_observation",
        description="Future-dated observation",
        available_at=as_of + timedelta(days=1),
    )

    package = DeterministicEvidencePackageBuilder().build(
        subject=subject,
        signal=signal,
        pattern=pattern,
        evidence=[future_evidence],
        as_of=as_of,
    )

    all_package_evidence = (
        package.constitutive_evidence + package.contextual_evidence
    )

    assert all_package_evidence == ()




def test_evidence_package_attributes_are_recursively_immutable():
    package = EvidencePackage(
        as_of=datetime(2026, 1, 15),
        subject_entity_id="entity:X",
        subject_name="X",
        subject_attributes={
            "profile": {
                "regions": ["US", "India"],
            },
        },
        signal_id="signal:test",
        signal_type="test_signal",
        signal_severity="high",
        signal_summary="Test signal",
        pattern_id="pattern:test",
        pattern_type="test_pattern",
        pattern_attributes={
            "thresholds": [10, 20],
        },
        constitutive_evidence=(),
        contextual_evidence=(),
    )

    with pytest.raises(TypeError):
        package.subject_attributes["new"] = "value"

    with pytest.raises(TypeError):
        package.subject_attributes["profile"]["new"] = "value"

    with pytest.raises(AttributeError):
        package.subject_attributes["profile"]["regions"].append("UK")

    with pytest.raises(AttributeError):
        package.pattern_attributes["thresholds"].append(30)
