from risksignal.intelligence.ai.contracts import (
    Finding,
    InvestigationResult,
)
from risksignal.intelligence.ai.testing import ConfiguredInvestigator

from test_ai_validation import _build_package


def test_configured_investigator_returns_configured_result():
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

    investigator = ConfiguredInvestigator(expected)

    actual = investigator.investigate(package)

    assert actual is expected
