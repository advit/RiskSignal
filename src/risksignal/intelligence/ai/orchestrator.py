from risksignal.intelligence.ai.contracts import (
    EvidencePackage,
    InvestigationResult,
    InvestigationValidator,
    ValidationReport,
    Investigator,
)


class InvestigationValidationError(Exception):
    """Raised when an investigation result fails deterministic validation."""

    def __init__(self, report: ValidationReport) -> None:
        self.report = report
        super().__init__(
            f"Investigation result failed validation with "
            f"{len(report.issues)} issue(s)."
        )


class InvestigationOrchestrator:
    """Coordinate investigation and deterministic result validation."""

    def __init__(
        self,
        *,
        investigator: Investigator,
        validator: InvestigationValidator,
    ) -> None:
        self.investigator = investigator
        self.validator = validator

    def investigate(
        self,
        package: EvidencePackage,
    ) -> InvestigationResult:
        result = self.investigator.investigate(package)
        report = self.validator.validate(package, result)

        if not report.ok:
            raise InvestigationValidationError(report)

        return result
