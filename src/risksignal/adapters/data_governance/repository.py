from __future__ import annotations

from risksignal.adapters.data_governance.models import (
    BusinessUnit,
    DataAsset,
    DataAssetOwnership,
    DqMeasurement,
    DqRule,
    Employee,
    GovernanceEvent,
)
from risksignal.persistence.duckdb_store import DuckDBStore


def persist_governance(store: DuckDBStore, seed: dict[str, list]) -> None:
    conn = store.conn
    conn.execute("DELETE FROM governance.dq_measurements")
    conn.execute("DELETE FROM governance.governance_events")
    conn.execute("DELETE FROM governance.data_asset_ownership")
    conn.execute("DELETE FROM governance.dq_rules")
    conn.execute("DELETE FROM governance.data_assets")
    conn.execute("DELETE FROM governance.employees")
    conn.execute("DELETE FROM governance.business_units")

    for unit in seed["business_units"]:
        conn.execute(
            "INSERT INTO governance.business_units VALUES (?, ?, ?, ?)",
            [unit.business_unit_id, unit.name, unit.parent_business_unit_id, unit.function],
        )
    for employee in seed["employees"]:
        conn.execute(
            "INSERT INTO governance.employees VALUES (?, ?, ?, ?, ?)",
            [
                employee.employee_id,
                employee.full_name,
                employee.business_unit_id,
                employee.role_title,
                employee.line,
            ],
        )
    for asset in seed["data_assets"]:
        conn.execute(
            "INSERT INTO governance.data_assets VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                asset.data_asset_id,
                asset.name,
                asset.description,
                asset.criticality,
                asset.lifecycle_state,
                asset.business_unit_id,
                asset.is_authoritative_source,
            ],
        )
    for item in seed["ownership"]:
        conn.execute(
            "INSERT INTO governance.data_asset_ownership VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                item.ownership_id,
                item.data_asset_id,
                item.employee_id,
                item.ownership_role,
                item.effective_from,
                item.effective_to,
                item.available_at,
            ],
        )
    for rule in seed["dq_rules"]:
        conn.execute(
            "INSERT INTO governance.dq_rules VALUES (?, ?, ?, ?, ?, ?)",
            [
                rule.dq_rule_id,
                rule.data_asset_id,
                rule.dimension,
                rule.name,
                rule.threshold,
                rule.weight,
            ],
        )
    for measurement in seed["dq_measurements"]:
        conn.execute(
            "INSERT INTO governance.dq_measurements VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [
                measurement.dq_measurement_id,
                measurement.dq_rule_id,
                measurement.data_asset_id,
                measurement.dimension,
                measurement.value,
                measurement.observed_at,
                measurement.available_at,
                measurement.recorded_at,
            ],
        )
    for event in seed["governance_events"]:
        conn.execute(
            "INSERT INTO governance.governance_events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                event.governance_event_id,
                event.data_asset_id,
                event.event_type,
                event.occurred_at,
                event.available_at,
                event.severity,
                event.status,
                event.description,
                event.recorded_at,
            ],
        )


def load_governance(store: DuckDBStore) -> dict[str, list]:
    conn = store.conn
    units = [
        BusinessUnit(r[0], r[1], r[3], r[2])
        for r in conn.execute("SELECT * FROM governance.business_units").fetchall()
    ]
    employees = [
        Employee(*r)
        for r in conn.execute("SELECT * FROM governance.employees").fetchall()
    ]
    assets = [
        DataAsset(*r)
        for r in conn.execute("SELECT * FROM governance.data_assets").fetchall()
    ]
    ownership = [
        DataAssetOwnership(*r)
        for r in conn.execute("SELECT * FROM governance.data_asset_ownership").fetchall()
    ]
    rules = [
        DqRule(*r) for r in conn.execute("SELECT * FROM governance.dq_rules").fetchall()
    ]
    measurements = [
        DqMeasurement(*r)
        for r in conn.execute("SELECT * FROM governance.dq_measurements").fetchall()
    ]
    events = [
        GovernanceEvent(*r)
        for r in conn.execute("SELECT * FROM governance.governance_events").fetchall()
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
