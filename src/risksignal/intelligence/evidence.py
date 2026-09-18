from __future__ import annotations

from uuid import uuid4

from risksignal.canonical.models import Evidence, Pattern, Signal
from risksignal.intelligence.context import Context


class EvidenceEngine:
    def collect(
        self,
        *,
        signal: Signal,
        pattern: Pattern,
        context: Context,
    ) -> list[Evidence]:
        items: list[Evidence] = []
        items.append(
            Evidence(
                evidence_id=f"evd:{uuid4()}",
                signal_id=signal.signal_id,
                referenced_object_type="pattern",
                referenced_id=pattern.pattern_id,
                role="detected_pattern",
                description=f"{pattern.pattern_type} on {pattern.attributes.get('metric_name')}",
                available_at=pattern.as_of,
            )
        )

        observation_ids = set(pattern.attributes.get("observation_ids", []))
        for obs in context.observations:
            in_pattern = obs.observation_id in observation_ids
            is_composite = obs.metric_name == "dq_score"
            if not in_pattern and not is_composite:
                continue
            items.append(
                Evidence(
                    evidence_id=f"evd:{uuid4()}",
                    signal_id=signal.signal_id,
                    referenced_object_type="observation",
                    referenced_id=obs.observation_id,
                    role="supporting_observation",
                    description=f"{obs.metric_name}={obs.value} observed_at={obs.observed_at.isoformat()}",
                    available_at=obs.available_at,
                )
            )

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
            if rel.relationship_type not in {"owner", "steward", "custodian", "owned_by_unit"}:
                continue
            items.append(
                Evidence(
                    evidence_id=f"evd:{uuid4()}",
                    signal_id=signal.signal_id,
                    referenced_object_type="relationship",
                    referenced_id=rel.relationship_id,
                    role="context_relationship",
                    description=f"{rel.relationship_type} {rel.from_entity_id}->{rel.to_entity_id}",
                    available_at=rel.available_at,
                )
            )
        return items
