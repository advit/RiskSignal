from __future__ import annotations

from datetime import datetime
from typing import Protocol

from risksignal.canonical.models import (
    Entity,
    Event,
    Evidence,
    Investigation,
    Observation,
    Pattern,
    Recommendation,
    Relationship,
    Signal,
)
from risksignal.intelligence.context import Context


class ContextBuilder(Protocol):
    def build(
        self,
        *,
        subject: Entity,
        relationships: list[Relationship],
        observations: list[Observation],
        events: list[Event],
        as_of: datetime,
    ) -> Context: ...


class PatternDetector(Protocol):
    def detect(self, context: Context, *, detected_at: datetime) -> list[Pattern]: ...


class SignalGenerator(Protocol):
    def emit(
        self,
        *,
        context: Context,
        patterns: list[Pattern],
        detected_at: datetime,
    ) -> list[Signal]: ...


class EvidenceConstructor(Protocol):
    def collect(
        self,
        *,
        signal: Signal,
        pattern: Pattern,
        patterns: list[Pattern],
        context: Context,
    ) -> list[Evidence]: ...


class InvestigationStage(Protocol):
    def build(
        self,
        *,
        signal: Signal,
        pattern: Pattern,
        evidence: list[Evidence],
        context: Context,
        created_at: datetime,
    ) -> Investigation: ...


class RecommendationStage(Protocol):
    def build(
        self,
        *,
        investigation_id: str,
        signal: Signal,
        evidence: list[Evidence],
        created_at: datetime,
    ) -> Recommendation: ...
