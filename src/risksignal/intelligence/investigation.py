from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from risksignal.canonical.models import Evidence, Investigation, Pattern, Signal
from risksignal.intelligence.context import Context
from risksignal.intelligence.evidence import CONSTITUTIVE_ROLES


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
        constitutive = [item for item in evidence if item.role in CONSTITUTIVE_ROLES]
        contextual = [item for item in evidence if item.role not in CONSTITUTIVE_ROLES]
        constitutive_lines = [f"- [{item.role}] {item.description}" for item in constitutive]
        context_lines = [f"- [{item.role}] {item.description}" for item in contextual]
        narrative = (
            f"Signal {signal.signal_type} for {context.subject.name} "
            f"(severity={signal.severity}) as of {context.as_of.isoformat()}. "
            f"Pattern {pattern.pattern_type}. "
            "Assessment uses only facts with available_at at or before as_of.\n"
            "Constitutive evidence:\n"
            + ("\n".join(constitutive_lines) if constitutive_lines else "- none")
            + "\nContextual evidence:\n"
            + ("\n".join(context_lines) if context_lines else "- none")
        )
        return Investigation(
            investigation_id=f"inv:{uuid4()}",
            signal_id=signal.signal_id,
            narrative=narrative,
            created_at=created_at,
            as_of=context.as_of,
        )
