from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from risksignal.canonical.models import Evidence, Recommendation, Signal


class RecommendationBuilder:
    def build(
        self,
        *,
        investigation_id: str,
        signal: Signal,
        evidence: list[Evidence],
        created_at: datetime,
    ) -> Recommendation:
        has_migration = any(
            item.role == "contextual_event" and "migration" in item.description.lower()
            for item in evidence
        )
        metric = signal.attributes.get("metric_name", "the deteriorating metric")
        if has_migration:
            action = (
                f"Increase monitoring frequency for {metric}, validate the in-progress migration control, "
                "and prioritize upstream processing stability before the next reporting cycle."
            )
        else:
            action = (
                f"Increase monitoring frequency for {metric} and review ownership accountability "
                "for the affected entity."
            )
        return Recommendation(
            recommendation_id=f"rec:{uuid4()}",
            investigation_id=investigation_id,
            action=action,
            rationale=signal.summary,
            created_at=created_at,
        )
