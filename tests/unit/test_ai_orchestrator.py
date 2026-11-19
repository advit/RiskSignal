import pytest

from risksignal.intelligence.ai.contracts import (
    Finding,
    InvestigationResult,
)
from risksignal.intelligence.ai.orchestrator import (
    InvestigationOrchestrator,
    InvestigationValidationError,
)
from risksignal.intelligence.ai.testing import ConfiguredInvestigator
from risksignal.intelligence.ai.validation import (
    DeterministicInvestigationValidator,
)

from test_ai_validation import _build_package


def test_orchestrator_returns_validated_investigation_result():
    package = _build_package()

    expected = InvestigationResult(
        summary="Test investigation summary.",
        findings=(
            Finding(
                statement="Test finding.",
                evidence_ids=("E001",),
            ),
        ),
        supporting_evidence_ids=("E001",),
        possible_explanations=(),
        unknowns=(),
        recommended_next_steps=(),
        confidence=0.8,
    )

    orchestrator = InvestigationOrchestrator(
        investigator=ConfiguredInvestigator(expected),
        validator=DeterministicInvestigationValidator(),
    )

    actual = orchestrator.investigate(package)

    assert actual is expected


def test_orchestrator_rejects_invalid_investigation_result():
    package = _build_package()

    invalid_result = InvestigationResult(
        summary="Test investigation summary.",
        findings=(
            Finding(
                statement="Unsupported finding.",
                evidence_ids=("UNKNOWN",),
            ),
        ),
        supporting_evidence_ids=("UNKNOWN",),
        possible_explanations=(),
        unknowns=(),
        recommended_next_steps=(),
        confidence=0.8,
    )

    orchestrator = InvestigationOrchestrator(
        investigator=ConfiguredInvestigator(invalid_result),
        validator=DeterministicInvestigationValidator(),
    )

    with pytest.raises(InvestigationValidationError) as exc_info:
        orchestrator.investigate(package)

    assert exc_info.value.report.ok is False
    assert len(exc_info.value.report.issues) > 0
