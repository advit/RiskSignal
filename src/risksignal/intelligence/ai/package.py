from __future__ import annotations

from datetime import datetime

from risksignal.canonical.models import (
    Entity,
    Evidence,
    Pattern,
    Signal,
)
from risksignal.intelligence.ai.contracts import (
    EvidencePackage,
    EvidenceRecord,
)
from risksignal.intelligence.evidence_roles import CONSTITUTIVE_ROLES


class DeterministicEvidencePackageBuilder:
    """Build a closed world AI evidence package from deterministic outputs."""

    def build(
        self,
        *,
        subject: Entity,
        signal: Signal,
        pattern: Pattern,
        evidence: list[Evidence],
        as_of: datetime,
    ) -> EvidencePackage:
        records = tuple(
            EvidenceRecord(
                evidence_id=item.evidence_id,
                role=item.role,
                referenced_object_type=item.referenced_object_type,
                referenced_id=item.referenced_id,
                description=item.description,
                available_at=item.available_at,
            )
            for item in evidence
            if item.available_at <= as_of
        )

        constitutive = tuple(
            item for item in records if item.role in CONSTITUTIVE_ROLES
        )

        contextual = tuple(
            item for item in records if item.role not in CONSTITUTIVE_ROLES
        )

        return EvidencePackage(
            as_of=as_of,
            subject_entity_id=subject.entity_id,
            subject_name=subject.name,
            subject_attributes=dict(subject.attributes),
            signal_id=signal.signal_id,
            signal_type=signal.signal_type,
            signal_severity=signal.severity,
            signal_summary=signal.summary,
            pattern_id=pattern.pattern_id,
            pattern_type=pattern.pattern_type,
            pattern_attributes=dict(pattern.attributes),
            constitutive_evidence=constitutive,
            contextual_evidence=contextual,
        )
