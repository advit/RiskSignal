from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from risksignal.canonical.models import Evidence, Investigation, Pattern, Signal
from risksignal.intelligence.context import Context


class InvestigationBuilder:
    def build(
        self,
        *,
        signal: Signal,
        pattern: Pattern,
        evidence: list[Evidence],
        context: Context,
        created_at: datetime,
    ) -> Investigation:
        metric = pattern.attributes.get("metric_name", "metric")
        event_types = sorted({item.description for item in evidence if item.role == "contextual_event"})
        observation_lines = [
            f"- {item.description}"
            for item in evidence
            if item.role == "supporting_observation"
        ][-8:]
        event_clause = (
            " Contextual events present: " + "; ".join(event_types) + "."
            if event_types
            else ""
        )
        narrative = (
            f"Signal {signal.signal_type} for {context.subject.name} "
            f"(severity={signal.severity}) as of {context.as_of.isoformat()}. "
            f"Detected pattern {pattern.pattern_type} on {metric} "
            f"from {pattern.attributes.get('start_value')} to {pattern.attributes.get('end_value')} "
            f"over {pattern.attributes.get('point_count')} eligible observations."
            f"{event_clause} "
            "Assessment uses only facts with available_at at or before as_of.\n"
            "Evidence:\n" + "\n".join(observation_lines)
        )
        return Investigation(
            investigation_id=f"inv:{uuid4()}",
            signal_id=signal.signal_id,
            narrative=narrative,
            created_at=created_at,
            as_of=context.as_of,
        )
