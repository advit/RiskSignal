from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


def _attrs() -> dict[str, Any]:
    return {}


@dataclass(frozen=True)
class Entity:
    entity_id: str
    entity_type: str
    name: str
    source_system: str
    source_id: str
    attributes: dict[str, Any] = field(default_factory=_attrs)


@dataclass(frozen=True)
class Relationship:
    relationship_id: str
    from_entity_id: str
    to_entity_id: str
    relationship_type: str
    available_at: datetime
    source_system: str
    source_id: str
    valid_from: datetime | None = None
    valid_to: datetime | None = None
    attributes: dict[str, Any] = field(default_factory=_attrs)

    def involves(self, entity_id: str) -> bool:
        return entity_id in (self.from_entity_id, self.to_entity_id)

    def is_active_at(self, as_of: datetime) -> bool:
        if self.available_at > as_of:
            return False
        if self.valid_from is not None and self.valid_from > as_of:
            return False
        if self.valid_to is not None and self.valid_to < as_of:
            return False
        return True


@dataclass(frozen=True)
class Observation:
    observation_id: str
    subject_entity_id: str
    observation_type: str
    metric_name: str
    value: float
    observed_at: datetime
    available_at: datetime
    source_system: str
    source_id: str
    attributes: dict[str, Any] = field(default_factory=_attrs)

    def is_eligible_at(self, as_of: datetime) -> bool:
        return self.available_at <= as_of


@dataclass(frozen=True)
class Event:
    event_id: str
    subject_entity_id: str
    event_type: str
    occurred_at: datetime
    available_at: datetime
    source_system: str
    source_id: str
    payload: dict[str, Any] = field(default_factory=_attrs)

    def is_eligible_at(self, as_of: datetime) -> bool:
        return self.available_at <= as_of


@dataclass(frozen=True)
class Pattern:
    pattern_id: str
    pattern_type: str
    subject_entity_id: str
    detected_at: datetime
    as_of: datetime
    window_start: datetime
    window_end: datetime
    attributes: dict[str, Any] = field(default_factory=_attrs)


@dataclass(frozen=True)
class Signal:
    signal_id: str
    subject_entity_id: str
    signal_type: str
    severity: str
    detected_at: datetime
    as_of: datetime
    pattern_id: str
    summary: str
    attributes: dict[str, Any] = field(default_factory=_attrs)


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    signal_id: str
    referenced_object_type: str
    referenced_id: str
    role: str
    description: str
    available_at: datetime


@dataclass(frozen=True)
class Investigation:
    investigation_id: str
    signal_id: str
    narrative: str
    created_at: datetime
    as_of: datetime


@dataclass(frozen=True)
class Recommendation:
    recommendation_id: str
    investigation_id: str
    action: str
    rationale: str
    created_at: datetime


@dataclass(frozen=True)
class Decision:
    decision_id: str
    recommendation_id: str
    decided_by: str
    decision_type: str
    decided_at: datetime
    notes: str = ""
