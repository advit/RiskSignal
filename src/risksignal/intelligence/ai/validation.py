from __future__ import annotations

from datetime import datetime

from math import isfinite

from risksignal.intelligence.ai.contracts import (
    EvidencePackage,
    EvidenceRecord,
    Finding,
    InvestigationResult,
    InvestigationValidator,
    ValidationIssue,
    ValidationReport,
)
from risksignal.intelligence.evidence_roles import CONSTITUTIVE_ROLES

class DeterministicInvestigationValidator(InvestigationValidator):
    """Validate AI investigation results against a closed evidence package."""

    def validate(
        self,
        package: EvidencePackage,
        result: InvestigationResult,
    ) -> ValidationReport:
        issues: list[ValidationIssue] = []

        if not isinstance(package, EvidencePackage):
            return ValidationReport(
                ok=False,
                issues=(
                    ValidationIssue(
                        code="malformed_input",
                        message="Evidence package must be an EvidencePackage object.",
                        path="package",
                    ),
                ),
            )

        if not isinstance(result, InvestigationResult):
            return ValidationReport(
                ok=False,
                issues=(
                    ValidationIssue(
                        code="malformed_output",
                        message="Investigation result must be an InvestigationResult object.",
                        path="result",
                    ),
                ),
            )

        evidence_collections = (
            package.constitutive_evidence,
            package.contextual_evidence,
        )

        if any(
            not isinstance(collection, (tuple, list))
            for collection in evidence_collections
        ):
            return ValidationReport(
                ok=False,
                issues=(
                    ValidationIssue(
                        code="malformed_input",
                        message="Evidence collections must be lists or tuples.",
                        path="evidence",
                    ),
                ),
            )

        if any(
            not isinstance(item, EvidenceRecord)
            for collection in evidence_collections
            for item in collection
        ):
            return ValidationReport(
                ok=False,
                issues=(
                    ValidationIssue(
                        code="malformed_input",
                        message="Every evidence entry must be an EvidenceRecord.",
                        path="evidence",
                    ),
                ),
            )

        malformed_records = [
            item
            for collection in evidence_collections
            for item in collection
            if (
                not isinstance(item.evidence_id, str)
                or not item.evidence_id.strip()
                or not isinstance(item.role, str)
                or not item.role.strip()
                or not isinstance(item.referenced_object_type, str)
                or not item.referenced_object_type.strip()
                or not isinstance(item.referenced_id, str)
                or not item.referenced_id.strip()
                or not isinstance(item.description, str)
                or not item.description.strip()
                or not isinstance(item.available_at, datetime)
            )
        ]

        if malformed_records:
            return ValidationReport(
                ok=False,
                issues=(
                    ValidationIssue(
                        code="malformed_input",
                        message=(
                            "Evidence record fields must contain "
                            "nonempty strings and a datetime."
                        ),
                        path="evidence",
                    ),
                ),
            )

        if not isinstance(package.as_of, datetime):
            return ValidationReport(
                ok=False,
                issues=(
                    ValidationIssue(
                        code="malformed_input",
                        message="Evidence package as_of must be a datetime.",
                        path="as_of",
                    ),
                ),
            )

        package_is_aware = package.as_of.utcoffset() is not None

        inconsistent_timestamps = [
            item
            for collection in evidence_collections
            for item in collection
            if (item.available_at.utcoffset() is not None)
            != package_is_aware
        ]

        if inconsistent_timestamps:
            return ValidationReport(
                ok=False,
                issues=(
                    ValidationIssue(
                        code="malformed_input",
                        message=(
                            "Evidence timestamps must use the same "
                            "timezone-awareness convention as package as_of."
                        ),
                        path="evidence",
                    ),
                ),
            )

        package_evidence = (
            package.constitutive_evidence
            + package.contextual_evidence
        )
        evidence_ids = [
            item.evidence_id for item in package_evidence
        ]

        if len(evidence_ids) != len(set(evidence_ids)):
            return ValidationReport(
                ok=False,
                issues=(
                    ValidationIssue(
                        code="duplicate_package_evidence_id",
                        message="Evidence package contains duplicate evidence IDs.",
                        path="evidence",
                    ),
                ),
            )

        role_mismatches = [
            item
            for item in package.constitutive_evidence
            if item.role not in CONSTITUTIVE_ROLES
        ] + [
            item
            for item in package.contextual_evidence
            if item.role in CONSTITUTIVE_ROLES
        ]

        if role_mismatches:
            return ValidationReport(
                ok=False,
                issues=(
                    ValidationIssue(
                        code="inconsistent_evidence_role",
                        message=(
                            "Evidence records must be placed in the "
                            "collection that matches their canonical role."
                        ),
                        path="evidence",
                    ),
                ),
            )
        evidence_by_id: dict[str, EvidenceRecord] = {
            item.evidence_id: item
            for item in package_evidence
        }
        constitutive_ids = {
            item.evidence_id
            for item in package.constitutive_evidence
        }

        self._validate_summary(result, issues)

        for field_name in (
            "possible_explanations",
            "unknowns",
            "recommended_next_steps",
        ):
            self._validate_text_collection(result, field_name, issues)

        self._validate_confidence(result, issues)
        self._validate_findings(
            result=result,
            evidence_by_id=evidence_by_id,
            constitutive_ids=constitutive_ids,
            issues=issues,
        )
        self._validate_supporting_evidence(
            result=result,
            evidence_by_id=evidence_by_id,
            issues=issues,
        )

        return ValidationReport(
            ok=not issues,
            issues=tuple(issues),
        )

    @staticmethod
    def _validate_summary(
        result: InvestigationResult,
        issues: list[ValidationIssue],
    ) -> None:
        if not isinstance(result.summary, str) or not result.summary.strip():
            issues.append(
                ValidationIssue(
                    code="malformed_output",
		    message="Investigation summary must be a nonempty string.",
		    path="summary",
                )
            )
    @staticmethod
    def _validate_text_collection(
        result: InvestigationResult,
        field_name: str,
        issues: list[ValidationIssue],
    ) -> None:
        values = getattr(result, field_name)

        if not isinstance(values, (tuple, list)):
            issues.append(
                ValidationIssue(
                    code="malformed_output",
                    message=f"{field_name} must be a list or tuple.",
                    path=field_name,
                )
            )
            return

        for index, value in enumerate(values):
            if not isinstance(value, str) or not value.strip():
                issues.append(
                    ValidationIssue(
                        code="malformed_output",
                        message=f"Every {field_name} entry must be a nonempty string.",
                        path=f"{field_name}[{index}]",
                    )
                )

    @staticmethod
    def _validate_confidence(
        result: InvestigationResult,
        issues: list[ValidationIssue],
    ) -> None:
        if isinstance(result.confidence, bool) or not isinstance(
            result.confidence, (int, float)
        ):
            issues.append(
                ValidationIssue(
                    code="malformed_output",
                    message="Confidence must be a numeric value between 0 and 1.",
                    path="confidence",
                )
            )
            return

        if not isfinite(result.confidence) or not 0.0 <= result.confidence <= 1.0:
            issues.append(
                ValidationIssue(
                    code="malformed_output",
                    message="Confidence must be between 0 and 1.",
                    path="confidence",
                )
            )

    @staticmethod
    def _validate_findings(
        *,
        result: InvestigationResult,
        evidence_by_id: dict[str, object],
        constitutive_ids: set[str],
        issues: list[ValidationIssue],
    ) -> None:
        if not isinstance(result.findings, (tuple, list)):
            issues.append(
                ValidationIssue(
                    code="malformed_output",
                    message="Findings must be a list or tuple.",
                    path="findings",
                )
            )
            return

        for index, finding in enumerate(result.findings):
            path = f"findings[{index}]"

            if not isinstance(finding, Finding):
                issues.append(
                    ValidationIssue(
                        code="malformed_output",
                        message="Each finding must be a Finding object.",
                        path=path,
                    )
                )
                continue

            if not isinstance(finding.statement, str) or not finding.statement.strip():
                issues.append(
                    ValidationIssue(
                        code="malformed_output",
                        message="Finding statement must be a nonempty string.",
                        path=f"{path}.statement",
                    )
                )

            if not isinstance(finding.evidence_ids, (tuple, list)):
                issues.append(
                    ValidationIssue(
                        code="malformed_output",
                        message="Finding evidence IDs must be a list or tuple.",
                        path=f"{path}.evidence_ids",
                    )
                )
                continue

            if not finding.evidence_ids:
                issues.append(
                    ValidationIssue(
                        code="unsupported_finding",
                        message="Every finding must cite at least one evidence ID.",
                        path=f"{path}.evidence_ids",
                    )
                )
                continue

            seen_ids: set[str] = set()

            for evidence_id in finding.evidence_ids:
                if not isinstance(evidence_id, str):
                    issues.append(
                        ValidationIssue(
                            code="malformed_output",
                            message="Finding evidence IDs must be strings.",
                            path=f"{path}.evidence_ids",
                        )
                    )
                    continue

                if not evidence_id:
                    issues.append(
                        ValidationIssue(
                            code="malformed_output",
                            message="Finding evidence IDs must not be empty.",
                            path=f"{path}.evidence_ids",
                        )
                    )
                    continue

                if evidence_id in seen_ids:
                    issues.append(
                        ValidationIssue(
                            code="malformed_output",
                            message="Finding evidence IDs must not contain duplicates.",
                            path=f"{path}.evidence_ids",
                        )
                    )
                    continue

                seen_ids.add(evidence_id)

                if evidence_id not in evidence_by_id:
                    issues.append(
                        ValidationIssue(
                            code="unknown_evidence_id",
                            message=(
                                f"Finding references evidence ID "
                                f"'{evidence_id}' that is not in the package."
                            ),
                            path=f"{path}.evidence_ids",
                        )
                    )

            known_ids = [
                evidence_id
                for evidence_id in finding.evidence_ids
                if isinstance(evidence_id, str)
                and evidence_id in evidence_by_id
            ]

            if known_ids and not any(
                evidence_id in constitutive_ids
                for evidence_id in known_ids
            ):
                issues.append(
                    ValidationIssue(
                        code="unsupported_finding",
                        message=(
                            "A finding must cite at least one constitutive "
                            "evidence item. Contextual evidence alone cannot "
                            "establish why the signal or pattern exists."
                        ),
                        path=f"{path}.evidence_ids",
                    )
                )

    @staticmethod
    def _validate_supporting_evidence(
        *,
        result: InvestigationResult,
        evidence_by_id: dict[str, object],
        issues: list[ValidationIssue],
    ) -> None:
        if not isinstance(result.supporting_evidence_ids, (tuple, list)):
            issues.append(
                ValidationIssue(
                    code="malformed_output",
                    message="Supporting evidence IDs must be a list or tuple.",
                    path="supporting_evidence_ids",
                )
            )
            return
        seen_ids: set[str] = set()

        for evidence_id in result.supporting_evidence_ids:
            if not isinstance(evidence_id, str):
                issues.append(
                    ValidationIssue(
                        code="malformed_output",
                        message="Supporting evidence IDs must be strings.",
                        path="supporting_evidence_ids",
                    )
                )
                continue

            if not evidence_id:
                issues.append(
                    ValidationIssue(
                        code="malformed_output",
                        message="Supporting evidence IDs must not be empty.",
                        path="supporting_evidence_ids",
                    )
                )
                continue

            if evidence_id in seen_ids:
                issues.append(
                    ValidationIssue(
                        code="malformed_output",
                        message="Supporting evidence IDs must not contain duplicates.",
                        path="supporting_evidence_ids",
                    )
                )
                continue

            seen_ids.add(evidence_id)

            if evidence_id not in evidence_by_id:
                issues.append(
                    ValidationIssue(
                        code="unknown_evidence_id",
                        message=(
                            f"Supporting evidence references evidence ID "
                            f"'{evidence_id}' that is not in the package."
                        ),
                        path="supporting_evidence_ids",
                    )
                )
