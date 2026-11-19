from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from risksignal.canonical.models import Entity, Event, Observation, Relationship


@dataclass(frozen=True)
class Context:
    subject: Entity
    as_of: datetime
    relationships: list[Relationship]
    observations: list[Observation]
    events: list[Event]
    historical_relationships: list[Relationship] = field(default_factory=list)


class ContextEngine:
    def build(
        self,
        *,
        subject: Entity,
        relationships: list[Relationship],
        observations: list[Observation],
        events: list[Event],
        as_of: datetime,
    ) -> Context:
        active: list[Relationship] = []
        historical: list[Relationship] = []
        for rel in relationships:
            if not rel.involves(subject.entity_id) or rel.available_at > as_of:
                continue
            if rel.is_active_at(as_of):
                active.append(rel)
            else:
                historical.append(rel)
        return Context(
            subject=subject,
            as_of=as_of,
            relationships=active,
            historical_relationships=historical,
            observations=[
                obs
                for obs in observations
                if obs.subject_entity_id == subject.entity_id and obs.is_eligible_at(as_of)
            ],
            events=[
                event
                for event in events
                if event.subject_entity_id == subject.entity_id and event.is_eligible_at(as_of)
            ],
        )
