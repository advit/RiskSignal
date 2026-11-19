from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Any, Protocol

from risksignal.canonical.models import (
    Entity,
    Evidence,
    Pattern,
    Signal,
)


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({
            key: _freeze(item)
            for key, item in value.items()
        })
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, (set, frozenset)):
        return frozenset(_freeze(item) for item in value)
    return value


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    role: str
    referenced_object_type: str
    referenced_id: str
    description: str
    available_at: datetime


@dataclass(frozen=True)
class EvidencePackage:
    as_of: datetime
    subject_entity_id: str
    subject_name: str
    subject_attributes: Mapping[str, Any]

    signal_id: str
    signal_type: str
    signal_severity: str
    signal_summary: str

    pattern_id: str
    pattern_type: str
    pattern_attributes: Mapping[str, Any]

    constitutive_evidence: tuple[EvidenceRecord, ...]
    contextual_evidence: tuple[EvidenceRecord, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "subject_attributes",
            _freeze(self.subject_attributes),
        )
        object.__setattr__(
            self,
            "pattern_attributes",
            _freeze(self.pattern_attributes),
        )


@dataclass(frozen=True)
class Finding:
    statement: str
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True)
class InvestigationResult:
    summary: str
    findings: tuple[Finding, ...]
    supporting_evidence_ids: tuple[str, ...]
    possible_explanations: tuple[str, ...]
    unknowns: tuple[str, ...]
    recommended_next_steps: tuple[str, ...]
    confidence: float


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    path: str


@dataclass(frozen=True)
class ValidationReport:
    ok: bool
    issues: tuple[ValidationIssue, ...]


class EvidencePackageBuilder(Protocol):
    def build(
        self,
        *,
        subject: Entity,
        signal: Signal,
        pattern: Pattern,
        evidence: list[Evidence],
        as_of: datetime,
    ) -> EvidencePackage: ...


class Investigator(Protocol):
    def investigate(
        self,
        package: EvidencePackage,
    ) -> InvestigationResult: ...


class InvestigationValidator(Protocol):
    def validate(
        self,
        package: EvidencePackage,
        result: InvestigationResult,
    ) -> ValidationReport: ...
