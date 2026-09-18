from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from risksignal.canonical.models import Pattern, Signal
from risksignal.intelligence.context import Context

CRITICALITY_VALUES = {"critical", "high"}


class SignalEngine:
    def emit(
        self,
        *,
        context: Context,
        patterns: list[Pattern],
        detected_at: datetime,
    ) -> list[Signal]:
        criticality = str(context.subject.attributes.get("criticality", "")).lower()
        signals: list[Signal] = []
        for pattern in patterns:
            if pattern.pattern_type != "consecutive_metric_decline":
                continue
            if criticality not in CRITICALITY_VALUES:
                continue
            metric = pattern.attributes.get("metric_name", "metric")
            start = pattern.attributes.get("start_value")
            end = pattern.attributes.get("end_value")
            signals.append(
                Signal(
                    signal_id=f"sig:{uuid4()}",
                    subject_entity_id=context.subject.entity_id,
                    signal_type="emerging_deterioration",
                    severity="high",
                    detected_at=detected_at,
                    as_of=context.as_of,
                    pattern_id=pattern.pattern_id,
                    summary=(
                        f"{context.subject.name} shows consecutive decline in {metric} "
                        f"from {start} to {end} as of {context.as_of.isoformat()}."
                    ),
                    attributes={"criticality": criticality, "metric_name": metric},
                )
            )
        return signals
