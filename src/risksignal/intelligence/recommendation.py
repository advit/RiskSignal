from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from risksignal.canonical.models import Evidence, Recommendation, Signal
from risksignal.intelligence.evidence_roles import CONSTITUTIVE_ROLES


class RecommendationBuilder:
    def build(
        self,
        *,
        investigation_id: str,
        signal: Signal,
        evidence: list[Evidence],
        created_at: datetime,
    ) -> Recommendation:
        contextual = [item for item in evidence if item.role not in CONSTITUTIVE_ROLES]
        has_migration_context = any(
            "migration" in item.description.lower() for item in contextual
        )
        parts: list[str] = []
        metric = signal.attributes.get("metric_name")
        required = signal.attributes.get("required_relationship_type")
        if signal.signal_type in {"emerging_deterioration", "compound_risk"}:
            label = metric or "the deteriorating metric"
            parts.append(f"Increase monitoring frequency for {label}.")
            if has_migration_context:
                parts.append(
                    "Validate the in-progress migration control, "
                    "and prioritize upstream processing stability before the next reporting cycle."
                )
        if signal.signal_type in {"missing_relationship", "compound_risk"}:
            rel = required or "required"
            parts.append(f"Restore an active '{rel}' relationship for the subject.")
        if not parts:
            parts.append("Review the constitutive evidence and confirm next action.")
        return Recommendation(
            recommendation_id=f"rec:{uuid4()}",
            investigation_id=investigation_id,
            action=" ".join(parts),
            rationale=signal.summary,
            created_at=created_at,
        )
