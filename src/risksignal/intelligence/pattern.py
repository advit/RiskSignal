from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from uuid import uuid4

from risksignal.canonical.models import Observation, Pattern
from risksignal.intelligence.context import Context

FAMILY_BY_PATTERN_TYPE = {
    "consecutive_metric_decline": "measurement_trend",
    "missing_relationship": "accountability",
}


class ConsecutiveMetricDeclineDetector:
    def __init__(self, min_consecutive: int = 5) -> None:
        self.min_consecutive = min_consecutive

    def detect(self, context: Context, *, detected_at: datetime) -> list[Pattern]:
        by_metric: dict[str, list[Observation]] = defaultdict(list)
        for obs in context.observations:
            by_metric[obs.metric_name].append(obs)

        found: list[Pattern] = []
        for metric_name, rows in by_metric.items():
            ordered = sorted(rows, key=lambda item: item.observed_at)
            run = _longest_strict_decline(ordered)
            if len(run) < self.min_consecutive:
                continue
            found.append(
                Pattern(
                    pattern_id=f"pat:{uuid4()}",
                    pattern_type="consecutive_metric_decline",
                    subject_entity_id=context.subject.entity_id,
                    detected_at=detected_at,
                    as_of=context.as_of,
                    window_start=run[0].observed_at,
                    window_end=run[-1].observed_at,
                    attributes={
                        "metric_name": metric_name,
                        "point_count": len(run),
                        "start_value": run[0].value,
                        "end_value": run[-1].value,
                        "observation_ids": [item.observation_id for item in run],
                    },
                )
            )
        return found


class MissingRelationshipDetector:
    def __init__(self, required_relationship_type: str) -> None:
        self.required_relationship_type = required_relationship_type

    def detect(self, context: Context, *, detected_at: datetime) -> list[Pattern]:
        required = self.required_relationship_type
        active = [
            rel
            for rel in context.relationships
            if rel.relationship_type == required
        ]
        if active:
            return []
        expired = [
            rel
            for rel in context.historical_relationships
            if rel.relationship_type == required
        ]
        timestamps = [rel.valid_to or rel.available_at for rel in expired]
        timestamps.append(context.as_of)
        return [
            Pattern(
                pattern_id=f"pat:{uuid4()}",
                pattern_type="missing_relationship",
                subject_entity_id=context.subject.entity_id,
                detected_at=detected_at,
                as_of=context.as_of,
                window_start=min(timestamps),
                window_end=context.as_of,
                attributes={
                    "required_relationship_type": required,
                    "active_count": 0,
                    "expired_relationship_ids": [rel.relationship_id for rel in expired],
                },
            )
        ]


class CompoundPatternComposer:
    def compose(
        self,
        patterns: list[Pattern],
        context: Context,
        *,
        detected_at: datetime,
    ) -> list[Pattern]:
        by_family: dict[str, list[Pattern]] = defaultdict(list)
        for pattern in patterns:
            family = FAMILY_BY_PATTERN_TYPE.get(pattern.pattern_type)
            if family is None or pattern.pattern_type == "compound":
                continue
            by_family[family].append(pattern)
        if len(by_family) < 2:
            return []
        representatives = [group[0] for group in by_family.values()]
        return [
            Pattern(
                pattern_id=f"pat:{uuid4()}",
                pattern_type="compound",
                subject_entity_id=context.subject.entity_id,
                detected_at=detected_at,
                as_of=context.as_of,
                window_start=min(item.window_start for item in representatives),
                window_end=max(item.window_end for item in representatives),
                attributes={
                    "component_pattern_ids": [item.pattern_id for item in representatives],
                    "component_types": [item.pattern_type for item in representatives],
                },
            )
        ]


class PatternEngine:
    def __init__(
        self,
        min_consecutive: int = 5,
        *,
        required_relationship_type: str | None = None,
        detectors: list | None = None,
    ) -> None:
        if detectors is not None:
            self._detectors = list(detectors)
        else:
            self._detectors = [ConsecutiveMetricDeclineDetector(min_consecutive)]
            if required_relationship_type is not None:
                self._detectors.append(
                    MissingRelationshipDetector(required_relationship_type)
                )
        self._composer = CompoundPatternComposer()

    def detect(self, context: Context, *, detected_at: datetime) -> list[Pattern]:
        atomic: list[Pattern] = []
        for detector in self._detectors:
            atomic.extend(detector.detect(context, detected_at=detected_at))
        return atomic + self._composer.compose(atomic, context, detected_at=detected_at)


def _longest_strict_decline(ordered: list[Observation]) -> list[Observation]:
    best: list[Observation] = []
    current: list[Observation] = []
    for item in ordered:
        if not current or item.value < current[-1].value:
            current.append(item)
        else:
            if len(current) > len(best):
                best = current
            current = [item]
    if len(current) > len(best):
        best = current
    return best
