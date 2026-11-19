from risksignal.intelligence.ai.contracts import (
    EvidencePackage,
    InvestigationResult,
    Investigator,
)


class ConfiguredInvestigator(Investigator):
    """Return a predetermined result for testing investigation workflows."""

    def __init__(self, result: InvestigationResult) -> None:
        self.result = result

    def investigate(
        self,
        package: EvidencePackage,
    ) -> InvestigationResult:
        return self.result
