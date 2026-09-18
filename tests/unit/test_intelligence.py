from datetime import datetime, timedelta

from risksignal.canonical.models import Entity, Observation
from risksignal.intelligence.context import ContextEngine
from risksignal.intelligence.pattern import PatternEngine
from risksignal.intelligence.signal import SignalEngine


def _subject(criticality: str) -> Entity:
    return Entity(
        entity_id="asset:X",
        entity_type="data_asset",
        name="X",
        source_system="test",
        source_id="X",
        attributes={"criticality": criticality},
    )


def _series(*, available_shift_days: int = 0) -> list[Observation]:
    rows = []
    for day in range(8):
        observed = datetime(2026, 1, 1) + timedelta(days=day)
        rows.append(
            Observation(
                observation_id=f"o{day}",
                subject_entity_id="asset:X",
                observation_type="metric",
                metric_name="timeliness",
                value=90 - day * 4,
                observed_at=observed,
                available_at=observed + timedelta(days=1 + available_shift_days),
                source_system="test",
                source_id=f"o{day}",
            )
        )
    return rows


def test_pattern_engine_detects_consecutive_decline():
    as_of = datetime(2026, 1, 10, 12, 0, 0)
    context = ContextEngine().build(
        subject=_subject("critical"),
        relationships=[],
        observations=_series(),
        events=[],
        as_of=as_of,
    )
    patterns = PatternEngine(min_consecutive=5).detect(context, detected_at=as_of)
    assert len(patterns) == 1
    assert patterns[0].pattern_type == "consecutive_metric_decline"
    assert patterns[0].attributes["metric_name"] == "timeliness"


def test_context_excludes_observations_not_yet_available():
    as_of = datetime(2026, 1, 5, 9, 0, 0)
    context = ContextEngine().build(
        subject=_subject("critical"),
        relationships=[],
        observations=_series(),
        events=[],
        as_of=as_of,
    )
    assert all(obs.available_at <= as_of for obs in context.observations)
    assert len(context.observations) < 8


def test_signal_requires_critical_subject():
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
