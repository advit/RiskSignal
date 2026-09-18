from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from uuid import uuid4

from risksignal.canonical.models import Observation, Pattern
from risksignal.intelligence.context import Context


class PatternEngine:
    def __init__(self, min_consecutive: int = 5) -> None:
        self.min_consecutive = min_consecutive

    def detect(self, context: Context, *, detected_at: datetime) -> list[Pattern]:
        patterns: list[Pattern] = []
        patterns.extend(self._consecutive_declines(context, detected_at))
        return patterns

    def _consecutive_declines(self, context: Context, detected_at: datetime) -> list[Pattern]:
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
