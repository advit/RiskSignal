from dataclasses import replace
from datetime import datetime, timedelta, timezone

from risksignal.canonical.models import Entity, Evidence, Pattern, Signal
from risksignal.intelligence.ai.contracts import (
    EvidencePackage,
    EvidenceRecord,
    Finding,
    InvestigationResult,
)
from risksignal.intelligence.ai.package import (
    DeterministicEvidencePackageBuilder,
)
from risksignal.intelligence.ai.validation import (
    DeterministicInvestigationValidator,
)


AS_OF = datetime(2026, 1, 15, 10, 0, 0)


def _build_package() -> EvidencePackage:
    subject = Entity(
        entity_id="DA047",
        entity_type="data_asset",
        name="Credit Exposure Amount",
        source_system="governance",
        source_id="DA047",
        attributes={"criticality": "high"},
    )
    signal = Signal(
        signal_id="S001",
        signal_type="compound_risk",
        severity="high",
        summary="Multiple indicators require investigation.",
        pattern_id="P001",
        subject_entity_id="DA047",
        detected_at=AS_OF,
        as_of=AS_OF,
    )
    pattern = Pattern(
    pattern_id="P001",
    pattern_type="compound",
    subject_entity_id="DA047",
    as_of=AS_OF,
    window_start=datetime(2025, 12, 1, 0, 0, 0),
    window_end=AS_OF,
    attributes={
        "component_pattern_ids": ("P010", "P011"),
        "component_types": (
            "consecutive_metric_decline",
            "missing_relationship",
            ),
        },
    detected_at=AS_OF,
    )
    evidence = [
    Evidence(
        evidence_id="E001",
        signal_id="S001",
        role="supporting_observation",
        referenced_object_type="observation",
        referenced_id="O001",
        description="Timeliness declined across consecutive measurements.",
        available_at=AS_OF,
    ),
    Evidence(
        evidence_id="E002",
        signal_id="S001",
        role="expired_relationship",
        referenced_object_type="relationship",
        referenced_id="R001",
        description="The accountable owner relationship expired.",
        available_at=AS_OF,
    ),
    Evidence(
        evidence_id="E003",
        signal_id="S001",
        role="contextual_event",
        referenced_object_type="event",
        referenced_id="EV001",
        description="The asset was involved in a migration event.",
        available_at=AS_OF,
    ),
]
    return DeterministicEvidencePackageBuilder().build(
        subject=subject,
        signal=signal,
        pattern=pattern,
        evidence=evidence,
        as_of=AS_OF,
    )


def test_valid_investigation_result_passes_validation():
    package = _build_package()

    result = InvestigationResult(
        summary=(
            "DA047 shows a sustained timeliness decline together with "
            "an expired accountable owner relationship."
        ),
        findings=(
            Finding(
                statement="Timeliness deteriorated across consecutive measurements.",
                evidence_ids=("E001",),
            ),
            Finding(
                statement="The accountable owner relationship is no longer active.",
                evidence_ids=("E002",),
            ),
        ),
        supporting_evidence_ids=("E001", "E002", "E003"),
        possible_explanations=(
            "The migration event may have contributed to the deterioration.",
        ),
        unknowns=(
            "The package does not establish whether a successor owner was assigned.",
        ),
        recommended_next_steps=(
            "Restore an active accountable owner and increase monitoring.",
        ),
        confidence=0.7,
    )

    report = DeterministicInvestigationValidator().validate(
        package,
        result,
    )

    assert report.ok is True
    assert report.issues == ()


def test_unknown_evidence_id_fails_validation():
    package = _build_package()

    result = InvestigationResult(
        summary="DA047 requires investigation.",
        findings=(
            Finding(
                statement="Timeliness deteriorated.",
                evidence_ids=("E999",),
            ),
        ),
        supporting_evidence_ids=(),
        possible_explanations=(),
        unknowns=(),
        recommended_next_steps=(),
        confidence=0.7,
    )

    report = DeterministicInvestigationValidator().validate(
        package,
        result,
    )

    assert report.ok is False
    assert any(
        issue.code == "unknown_evidence_id"
        for issue in report.issues
    )


def test_finding_without_evidence_fails_validation():
    package = _build_package()

    result = InvestigationResult(
        summary="DA047 requires investigation.",
        findings=(
            Finding(
                statement="Timeliness deteriorated.",
                evidence_ids=(),
            ),
        ),
        supporting_evidence_ids=(),
        possible_explanations=(),
        unknowns=(),
        recommended_next_steps=(),
        confidence=0.7,
    )

    report = DeterministicInvestigationValidator().validate(
        package,
        result,
    )

    assert report.ok is False
    assert any(
        issue.code == "unsupported_finding"
        for issue in report.issues
    )


def test_invalid_confidence_fails_validation():
    package = _build_package()

    result = InvestigationResult(
        summary="DA047 requires investigation.",
        findings=(),
        supporting_evidence_ids=(),
        possible_explanations=(),
        unknowns=(),
        recommended_next_steps=(),
        confidence=1.5,
    )

    report = DeterministicInvestigationValidator().validate(
        package,
        result,
    )

    assert report.ok is False
    assert any(
        issue.code == "malformed_output"
        and issue.path == "confidence"
        for issue in report.issues
    )
def test_boolean_confidence_fails_validation():
    package = _build_package()

    result = InvestigationResult(
        summary="DA047 requires investigation.",
        findings=(),
        supporting_evidence_ids=(),
        possible_explanations=(),
        unknowns=(),
        recommended_next_steps=(),
        confidence=True,
    )

    report = DeterministicInvestigationValidator().validate(
        package,
        result,
    )

    assert report.ok is False
    assert any(
        issue.code == "malformed_output"
        and issue.path == "confidence"
        for issue in report.issues
    )

def test_missing_summary_fails_validation():
    package = _build_package()

    result = InvestigationResult(
        summary="",
        findings=(),
        supporting_evidence_ids=(),
        possible_explanations=(),
        unknowns=(),
        recommended_next_steps=(),
        confidence=0.7,
    )

    report = DeterministicInvestigationValidator().validate(
        package,
        result,
    )

    assert report.ok is False
    assert any(
        issue.code == "malformed_output"
        and issue.path == "summary"
        for issue in report.issues
    )


def test_contextual_evidence_alone_cannot_support_finding():
    package = _build_package()

    result = InvestigationResult(
        summary="A migration event occurred for DA047.",
        findings=(
            Finding(
                statement="The migration caused the compound signal.",
                evidence_ids=("E003",),
            ),
        ),
        supporting_evidence_ids=("E003",),
        possible_explanations=(),
        unknowns=(),
        recommended_next_steps=(),
        confidence=0.7,
    )

    report = DeterministicInvestigationValidator().validate(
        package,
        result,
    )

    assert report.ok is False
    assert any(
        issue.code == "unsupported_finding"
        for issue in report.issues
    )


def test_supporting_evidence_must_exist_in_package():
    package = _build_package()

    result = InvestigationResult(
        summary="DA047 requires investigation.",
        findings=(),
        supporting_evidence_ids=("E001", "E999"),
        possible_explanations=(),
        unknowns=(),
        recommended_next_steps=(),
        confidence=0.7,
    )

    report = DeterministicInvestigationValidator().validate(
        package,
        result,
    )

    assert report.ok is False
    assert any(
        issue.code == "unknown_evidence_id"
        and issue.path == "supporting_evidence_ids"
        for issue in report.issues
    )
def test_duplicate_evidence_ids_in_package_fail_validation():
    package = _build_package()
    duplicate = package.constitutive_evidence[0]

    package = replace(
        package,
        contextual_evidence=package.contextual_evidence + (duplicate,),
    )

    result = InvestigationResult(
        summary="DA047 requires investigation.",
        findings=(),
        supporting_evidence_ids=(),
        possible_explanations=(),
        unknowns=(),
        recommended_next_steps=(),
        confidence=0.7,
    )

    report = DeterministicInvestigationValidator().validate(
        package,
        result,
    )

    assert report.ok is False
    assert any(
        issue.code == "duplicate_package_evidence_id"
        and issue.path == "evidence"
        for issue in report.issues
    )
def test_none_findings_fails_validation_without_crashing():
    package = _build_package()

    result = InvestigationResult(
        summary="DA047 requires investigation.",
        findings=None,
        supporting_evidence_ids=(),
        possible_explanations=(),
        unknowns=(),
        recommended_next_steps=(),
        confidence=0.7,
    )

    report = DeterministicInvestigationValidator().validate(
        package,
        result,
    )

    assert report.ok is False
    assert any(
        issue.code == "malformed_output"
        and issue.path == "findings"
        for issue in report.issues
    )
def test_invalid_finding_object_fails_validation_without_crashing():
    package = _build_package()

    result = InvestigationResult(
        summary="DA047 requires investigation.",
        findings=(None,),
        supporting_evidence_ids=(),
        possible_explanations=(),
        unknowns=(),
        recommended_next_steps=(),
        confidence=0.7,
    )

    report = DeterministicInvestigationValidator().validate(
        package,
        result,
    )

    assert report.ok is False
    assert any(
        issue.code == "malformed_output"
        and issue.path == "findings[0]"
        for issue in report.issues
    )
def test_none_supporting_evidence_ids_fails_validation_without_crashing():
    package = _build_package()

    result = InvestigationResult(
        summary="DA047 requires investigation.",
        findings=(),
        supporting_evidence_ids=None,
        possible_explanations=(),
        unknowns=(),
        recommended_next_steps=(),
        confidence=0.7,
    )

    report = DeterministicInvestigationValidator().validate(
        package,
        result,
    )

    assert report.ok is False
    assert any(
        issue.code == "malformed_output"
        and issue.path == "supporting_evidence_ids"
        for issue in report.issues
    )
def test_none_possible_explanations_fails_validation_without_crashing():
    package = _build_package()

    result = InvestigationResult(
        summary="DA047 requires investigation.",
        findings=(),
        supporting_evidence_ids=(),
        possible_explanations=None,
        unknowns=(),
        recommended_next_steps=(),
        confidence=0.7,
    )

    report = DeterministicInvestigationValidator().validate(
        package,
        result,
    )

    assert report.ok is False
    assert any(
        issue.code == "malformed_output"
        and issue.path == "possible_explanations"
        for issue in report.issues
    )
def test_none_unknowns_fails_validation():
    package = _build_package()

    result = InvestigationResult(
        summary="DA047 requires investigation.",
        findings=(),
        supporting_evidence_ids=(),
        possible_explanations=(),
        unknowns=None,
        recommended_next_steps=(),
        confidence=0.7,
    )

    report = DeterministicInvestigationValidator().validate(package, result)

    assert report.ok is False
    assert any(
        issue.code == "malformed_output" and issue.path == "unknowns"
        for issue in report.issues
    )


def test_none_recommended_next_steps_fails_validation():
    package = _build_package()

    result = InvestigationResult(
        summary="DA047 requires investigation.",
        findings=(),
        supporting_evidence_ids=(),
        possible_explanations=(),
        unknowns=(),
        recommended_next_steps=None,
        confidence=0.7,
    )

    report = DeterministicInvestigationValidator().validate(package, result)

    assert report.ok is False
    assert any(
        issue.code == "malformed_output"
        and issue.path == "recommended_next_steps"
        for issue in report.issues
    )
def test_empty_possible_explanation_fails_validation():
    package = _build_package()

    result = InvestigationResult(
        summary="DA047 requires investigation.",
        findings=(),
        supporting_evidence_ids=(),
        possible_explanations=(" ",),
        unknowns=(),
        recommended_next_steps=(),
        confidence=0.7,
    )

    report = DeterministicInvestigationValidator().validate(package, result)

    assert report.ok is False
    assert any(
        issue.code == "malformed_output"
        and issue.path == "possible_explanations[0]"
        for issue in report.issues
    )
def test_none_finding_evidence_ids_fails_validation_without_crashing():
    package = _build_package()

    finding = Finding(
        statement="Timeliness deteriorated.",
        evidence_ids=None,
    )

    result = InvestigationResult(
        summary="DA047 requires investigation.",
        findings=(finding,),
        supporting_evidence_ids=(),
        possible_explanations=(),
        unknowns=(),
        recommended_next_steps=(),
        confidence=0.7,
    )

    report = DeterministicInvestigationValidator().validate(package, result)

    assert report.ok is False
    assert any(
        issue.code == "malformed_output"
        and issue.path == "findings[0].evidence_ids"
        for issue in report.issues
    )
def test_string_finding_evidence_ids_fails_validation():
    package = _build_package()

    finding = Finding(
        statement="Timeliness deteriorated.",
        evidence_ids="E001",
    )

    result = InvestigationResult(
        summary="DA047 requires investigation.",
        findings=(finding,),
        supporting_evidence_ids=(),
        possible_explanations=(),
        unknowns=(),
        recommended_next_steps=(),
        confidence=0.7,
    )

    report = DeterministicInvestigationValidator().validate(package, result)

    assert report.ok is False
    assert any(
        issue.code == "malformed_output"
        and issue.path == "findings[0].evidence_ids"
        for issue in report.issues
    )
def test_non_string_finding_evidence_id_fails_validation():
    package = _build_package()

    finding = Finding(
        statement="Timeliness deteriorated.",
        evidence_ids=(123,),
    )

    result = InvestigationResult(
        summary="DA047 requires investigation.",
        findings=(finding,),
        supporting_evidence_ids=(),
        possible_explanations=(),
        unknowns=(),
        recommended_next_steps=(),
        confidence=0.7,
    )

    report = DeterministicInvestigationValidator().validate(package, result)

    assert report.ok is False
    assert any(
        issue.code == "malformed_output"
        and issue.path == "findings[0].evidence_ids"
        for issue in report.issues
    )
def test_unhashable_finding_evidence_id_fails_validation_without_crashing():
    package = _build_package()

    finding = Finding(
        statement="Timeliness deteriorated.",
        evidence_ids=([123],),
    )

    result = InvestigationResult(
        summary="DA047 requires investigation.",
        findings=(finding,),
        supporting_evidence_ids=(),
        possible_explanations=(),
        unknowns=(),
        recommended_next_steps=(),
        confidence=0.7,
    )

    report = DeterministicInvestigationValidator().validate(package, result)

    assert report.ok is False
    assert any(
        issue.code == "malformed_output"
        and issue.path == "findings[0].evidence_ids"
        for issue in report.issues
    )
def test_non_string_supporting_evidence_id_fails_validation():
    package = _build_package()

    result = InvestigationResult(
        summary="DA047 requires investigation.",
        findings=(),
        supporting_evidence_ids=(123,),
        possible_explanations=(),
        unknowns=(),
        recommended_next_steps=(),
        confidence=0.7,
    )

    report = DeterministicInvestigationValidator().validate(package, result)

    assert report.ok is False
    assert any(
        issue.code == "malformed_output"
        and issue.path == "supporting_evidence_ids"
        for issue in report.issues
    )
def test_unhashable_supporting_evidence_id_fails_validation_without_crashing():
    package = _build_package()

    result = InvestigationResult(
        summary="DA047 requires investigation.",
        findings=(),
        supporting_evidence_ids=([123],),
        possible_explanations=(),
        unknowns=(),
        recommended_next_steps=(),
        confidence=0.7,
    )

    report = DeterministicInvestigationValidator().validate(package, result)

    assert report.ok is False
    assert any(
        issue.code == "malformed_output"
        and issue.path == "supporting_evidence_ids"
        for issue in report.issues
    )

def test_invalid_investigation_result_object_fails_validation_without_crashing():
    package = _build_package()

    report = DeterministicInvestigationValidator().validate(
        package,
        None,
    )

    assert report.ok is False
    assert any(
        issue.code == "malformed_output"
        and issue.path == "result"
        for issue in report.issues
    )
def test_invalid_evidence_package_fails_validation_without_crashing():
    report = DeterministicInvestigationValidator().validate(
        None,
        InvestigationResult(
            summary="DA047 requires investigation.",
            findings=(),
            supporting_evidence_ids=(),
            possible_explanations=(),
            unknowns=(),
            recommended_next_steps=(),
            confidence=0.7,
        ),
    )

    assert report.ok is False
    assert any(
        issue.code == "malformed_input"
        and issue.path == "package"
        for issue in report.issues
    )


def test_contextual_role_cannot_be_classified_as_constitutive():
    package = _build_package()
    contextual = package.contextual_evidence[0]

    package = replace(
        package,
        constitutive_evidence=(
            package.constitutive_evidence + (contextual,)
        ),
        contextual_evidence=(),
    )

    result = InvestigationResult(
        summary="A migration event caused the signal.",
        findings=(
            Finding(
                statement="The migration event caused the signal.",
                evidence_ids=("E003",),
            ),
        ),
        supporting_evidence_ids=("E003",),
        possible_explanations=(),
        unknowns=(),
        recommended_next_steps=(),
        confidence=0.7,
    )

    report = DeterministicInvestigationValidator().validate(
        package,
        result,
    )

    assert report.ok is False
    assert any(
        issue.code == "inconsistent_evidence_role"
        for issue in report.issues
    )

def test_malformed_evidence_record_fails_validation_without_crashing():
    package = _build_package()

    package = replace(
        package,
        constitutive_evidence=("not-an-evidence-record",),
    )

    result = InvestigationResult(
        summary="Investigation completed.",
        findings=(),
        supporting_evidence_ids=(),
        possible_explanations=(),
        unknowns=(),
        recommended_next_steps=(),
        confidence=0.5,
    )

    report = DeterministicInvestigationValidator().validate(
        package,
        result,
    )

    assert report.ok is False
    assert any(
        issue.code == "malformed_input"
        and issue.path == "evidence"
        for issue in report.issues
    )


def test_none_evidence_collection_fails_validation_without_crashing():
    package = _build_package()

    package = replace(
        package,
        constitutive_evidence=None,
    )

    result = InvestigationResult(
        summary="Investigation completed.",
        findings=(),
        supporting_evidence_ids=(),
        possible_explanations=(),
        unknowns=(),
        recommended_next_steps=(),
        confidence=0.5,
    )

    report = DeterministicInvestigationValidator().validate(
        package,
        result,
    )

    assert report.ok is False
    assert any(
        issue.code == "malformed_input"
        and issue.path == "evidence"
        for issue in report.issues
    )

def test_non_string_evidence_record_id_fails_validation():
    package = _build_package()
    malformed_record = replace(
        package.constitutive_evidence[0],
        evidence_id=None,
    )

    package = replace(
        package,
        constitutive_evidence=(
            malformed_record,
            *package.constitutive_evidence[1:],
        ),
    )

    result = InvestigationResult(
        summary="Investigation completed.",
        findings=(),
        supporting_evidence_ids=(),
        possible_explanations=(),
        unknowns=(),
        recommended_next_steps=(),
        confidence=0.5,
    )

    report = DeterministicInvestigationValidator().validate(
        package,
        result,
    )

    assert report.ok is False
    assert any(
        issue.code == "malformed_input"
        and issue.path == "evidence"
        for issue in report.issues
    )

def test_mixed_timezone_awareness_in_evidence_fails_validation():
    package = _build_package()

    malformed_record = replace(
        package.constitutive_evidence[0],
        available_at=datetime(2026, 1, 15, 10, 0, 0, tzinfo=timezone.utc),
    )

    package = replace(
        package,
        constitutive_evidence=(
            malformed_record,
            *package.constitutive_evidence[1:],
        ),
    )

    result = InvestigationResult(
        summary="Investigation completed.",
        findings=(),
        supporting_evidence_ids=(),
        possible_explanations=(),
        unknowns=(),
        recommended_next_steps=(),
        confidence=0.5,
    )

    report = DeterministicInvestigationValidator().validate(
        package,
        result,
    )

    assert report.ok is False
    assert any(
        issue.code == "malformed_input"
        and issue.path == "evidence"
        for issue in report.issues
    )

def test_different_aware_timezone_offsets_pass_validation():
    package = _build_package()

    package = replace(
        package,
        as_of=package.as_of.replace(tzinfo=timezone.utc),
        constitutive_evidence=tuple(
            replace(
                item,
                available_at=item.available_at.replace(
                    tzinfo=timezone(timedelta(hours=5, minutes=30))
                ),
            )
            for item in package.constitutive_evidence
        ),
        contextual_evidence=tuple(
            replace(
                item,
                available_at=item.available_at.replace(
                    tzinfo=timezone(timedelta(hours=5, minutes=30))
                ),
            )
            for item in package.contextual_evidence
        ),
    )

    result = InvestigationResult(
        summary="Investigation completed.",
        findings=(),
        supporting_evidence_ids=(),
        possible_explanations=(),
        unknowns=(),
        recommended_next_steps=(),
        confidence=0.5,
    )

    report = DeterministicInvestigationValidator().validate(
        package,
        result,
    )

    assert report.ok is True
    assert report.issues == ()
