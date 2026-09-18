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
        signals: list[Signal] = []
        for pattern in patterns:
            signal = _signal_for_pattern(context, pattern, patterns, detected_at)
            if signal is not None:
                signals.append(signal)
        return signals


def _signal_for_pattern(
    context: Context,
    pattern: Pattern,
    patterns: list[Pattern],
    detected_at: datetime,
) -> Signal | None:
    criticality = str(context.subject.attributes.get("criticality", "")).lower()
    if pattern.pattern_type == "consecutive_metric_decline":
        if criticality not in CRITICALITY_VALUES:
            return None
        metric = pattern.attributes.get("metric_name", "metric")
        return Signal(
            signal_id=f"sig:{uuid4()}",
            subject_entity_id=context.subject.entity_id,
            signal_type="emerging_deterioration",
            severity="high",
            detected_at=detected_at,
            as_of=context.as_of,
            pattern_id=pattern.pattern_id,
            summary=(
                f"{context.subject.name} shows consecutive decline in {metric} "
                f"from {pattern.attributes.get('start_value')} to {pattern.attributes.get('end_value')} "
                f"as of {context.as_of.isoformat()}."
            ),
            attributes={"criticality": criticality, "metric_name": metric},
        )
    if pattern.pattern_type == "missing_relationship":
        required = pattern.attributes.get("required_relationship_type", "relationship")
        severity = "high" if criticality in CRITICALITY_VALUES else "medium"
        return Signal(
            signal_id=f"sig:{uuid4()}",
            subject_entity_id=context.subject.entity_id,
            signal_type="missing_relationship",
            severity=severity,
            detected_at=detected_at,
            as_of=context.as_of,
            pattern_id=pattern.pattern_id,
            summary=(
                f"{context.subject.name} has no active '{required}' relationship "
                f"as of {context.as_of.isoformat()}."
            ),
            attributes={
                "criticality": criticality,
                "required_relationship_type": required,
            },
        )
    if pattern.pattern_type == "compound":
        types = pattern.attributes.get("component_types", [])
        child_ids = set(pattern.attributes.get("component_pattern_ids", []))
        children = [item for item in patterns if item.pattern_id in child_ids]
        metric = next(
            (
                child.attributes.get("metric_name")
                for child in children
                if child.pattern_type == "consecutive_metric_decline"
            ),
            None,
        )
        required = next(
            (
                child.attributes.get("required_relationship_type")
                for child in children
                if child.pattern_type == "missing_relationship"
            ),
            None,
        )
        attributes: dict = {
            "criticality": criticality,
            "component_types": types,
            "component_pattern_ids": pattern.attributes.get("component_pattern_ids", []),
        }
        if metric is not None:
            attributes["metric_name"] = metric
        if required is not None:
            attributes["required_relationship_type"] = required
        return Signal(
            signal_id=f"sig:{uuid4()}",
            subject_entity_id=context.subject.entity_id,
            signal_type="compound_risk",
            severity="high",
            detected_at=detected_at,
            as_of=context.as_of,
            pattern_id=pattern.pattern_id,
            summary=(
                f"{context.subject.name} has independent indicators "
                f"{', '.join(types)} as of {context.as_of.isoformat()}."
            ),
            attributes=attributes,
        )
    return None
