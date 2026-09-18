from __future__ import annotations

from datetime import datetime, timedelta

from risksignal.adapters.data_governance.models import (
    BusinessUnit,
    DataAsset,
    DataAssetOwnership,
    DqMeasurement,
    DqRule,
    Employee,
    GovernanceEvent,
)

ASSET_ID = "DA047"
N_DAYS = 14
FUTURE_DAY_OFFSET = 14


def morning(day: datetime) -> datetime:
    return datetime(day.year, day.month, day.day, 9, 0, 0)


def demo_as_of() -> datetime:
    """After day-13 measurements are available; before the future leak row."""
    last_observed = datetime(2026, 1, 1) + timedelta(days=N_DAYS - 1)
    return morning(last_observed + timedelta(days=1)) + timedelta(hours=1)


def build_seed() -> dict[str, list]:
    start = datetime(2026, 1, 1)
    units = [
        BusinessUnit("BU-RISK", "Enterprise Risk", "risk"),
        BusinessUnit("BU-GOV", "Data Governance", "second_line"),
    ]
    employees = [
        Employee("EMP-001", "Priya Shah", "BU-RISK", "Data Owner", "first"),
        Employee("EMP-002", "James Okonkwo", "BU-RISK", "Data Steward", "first"),
        Employee("EMP-003", "Elena Rossi", "BU-GOV", "Governance Lead", "second"),
    ]
    assets = [
        DataAsset(
            ASSET_ID,
            "Credit Exposure Amount",
            "Enterprise credit exposure used in risk and regulatory reporting.",
            "critical",
            "migration",
            "BU-RISK",
            True,
        )
    ]
    ownership = [
        DataAssetOwnership(
            "OWN-001",
            ASSET_ID,
            "EMP-001",
            "owner",
            start,
            None,
            morning(start),
        ),
        DataAssetOwnership(
            "OWN-002",
            ASSET_ID,
            "EMP-002",
            "steward",
            start,
            None,
            morning(start),
        ),
    ]
    rules = [
        DqRule("DQ-COMP", ASSET_ID, "completeness", "Required fields present", 95.0, 0.30),
        DqRule("DQ-ACC", ASSET_ID, "accuracy", "Reconcile to Exposure_Master", 95.0, 0.30),
        DqRule("DQ-TIME", ASSET_ID, "timeliness", "Available within SLA", 90.0, 0.20),
        DqRule("DQ-UNIQ", ASSET_ID, "uniqueness", "No duplicate exposure keys", 98.0, 0.20),
    ]

    measurements: list[DqMeasurement] = []
    completeness, accuracy, duplicate_rate = 92.0, 85.0, 3.0
    uniqueness = 100.0 - duplicate_rate
    for day in range(N_DAYS):
        observed = start + timedelta(days=day)
        available = morning(observed + timedelta(days=1))
        recorded = available
        timeliness = 90.0 - (day * 3.0)
        dims = {
            "completeness": ("DQ-COMP", completeness),
            "accuracy": ("DQ-ACC", accuracy),
            "timeliness": ("DQ-TIME", timeliness),
            "uniqueness": ("DQ-UNIQ", uniqueness),
        }
        for dimension, (rule_id, value) in dims.items():
            measurements.append(
                DqMeasurement(
                    dq_measurement_id=f"M-{dimension[:4].upper()}-{observed.date().isoformat()}",
                    dq_rule_id=rule_id,
                    data_asset_id=ASSET_ID,
                    dimension=dimension,
                    value=value,
                    observed_at=observed,
                    available_at=available,
                    recorded_at=recorded,
                )
            )

    future_observed = start + timedelta(days=FUTURE_DAY_OFFSET)
    future_available = morning(future_observed + timedelta(days=5))
    measurements.append(
        DqMeasurement(
            dq_measurement_id="M-TIME-FUTURE",
            dq_rule_id="DQ-TIME",
            data_asset_id=ASSET_ID,
            dimension="timeliness",
            value=10.0,
            observed_at=future_observed,
            available_at=future_available,
            recorded_at=future_available,
        )
    )

    events = [
        GovernanceEvent(
            governance_event_id="GOV-MIG-001",
            data_asset_id=ASSET_ID,
            event_type="migration",
            occurred_at=datetime(2026, 1, 5, 8, 0, 0),
            available_at=morning(datetime(2026, 1, 5)),
            severity="medium",
            status="in_progress",
            description="Platform migration of upstream ingestion for DA047.",
            recorded_at=morning(datetime(2026, 1, 5)),
        )
    ]
    return {
        "business_units": units,
        "employees": employees,
        "data_assets": assets,
        "ownership": ownership,
        "dq_rules": rules,
        "dq_measurements": measurements,
        "governance_events": events,
    }
