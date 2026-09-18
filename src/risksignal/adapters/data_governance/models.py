from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class BusinessUnit:
    business_unit_id: str
    name: str
    function: str
    parent_business_unit_id: str | None = None


@dataclass(frozen=True)
class Employee:
    employee_id: str
    full_name: str
    business_unit_id: str
    role_title: str
    line: str


@dataclass(frozen=True)
class DataAsset:
    data_asset_id: str
    name: str
    description: str
    criticality: str
    lifecycle_state: str
    business_unit_id: str
    is_authoritative_source: bool


@dataclass(frozen=True)
class DataAssetOwnership:
    ownership_id: str
    data_asset_id: str
    employee_id: str
    ownership_role: str
    effective_from: datetime
    effective_to: datetime | None
    available_at: datetime


@dataclass(frozen=True)
class DqRule:
    dq_rule_id: str
    data_asset_id: str
    dimension: str
    name: str
    threshold: float
    weight: float


@dataclass(frozen=True)
class DqMeasurement:
    dq_measurement_id: str
    dq_rule_id: str
    data_asset_id: str
    dimension: str
    value: float
    observed_at: datetime
    available_at: datetime
    recorded_at: datetime


@dataclass(frozen=True)
class GovernanceEvent:
    governance_event_id: str
    data_asset_id: str
    event_type: str
    occurred_at: datetime
    available_at: datetime
    severity: str
    status: str
    description: str
    recorded_at: datetime
