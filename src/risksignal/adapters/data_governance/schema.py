"""Data Governance domain tables. Intelligence must not import this module."""

GOVERNANCE_SCHEMA_SQL = """
CREATE SCHEMA IF NOT EXISTS governance;

CREATE TABLE IF NOT EXISTS governance.business_units (
    business_unit_id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    parent_business_unit_id VARCHAR,
    function VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS governance.employees (
    employee_id VARCHAR PRIMARY KEY,
    full_name VARCHAR NOT NULL,
    business_unit_id VARCHAR NOT NULL,
    role_title VARCHAR NOT NULL,
    line VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS governance.data_assets (
    data_asset_id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    criticality VARCHAR NOT NULL,
    lifecycle_state VARCHAR NOT NULL,
    business_unit_id VARCHAR NOT NULL,
    is_authoritative_source BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS governance.data_asset_ownership (
    ownership_id VARCHAR PRIMARY KEY,
    data_asset_id VARCHAR NOT NULL,
    employee_id VARCHAR NOT NULL,
    ownership_role VARCHAR NOT NULL,
    effective_from TIMESTAMP NOT NULL,
    effective_to TIMESTAMP,
    available_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS governance.dq_rules (
    dq_rule_id VARCHAR PRIMARY KEY,
    data_asset_id VARCHAR NOT NULL,
    dimension VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
    threshold DOUBLE NOT NULL,
    weight DOUBLE NOT NULL
);

CREATE TABLE IF NOT EXISTS governance.dq_measurements (
    dq_measurement_id VARCHAR PRIMARY KEY,
    dq_rule_id VARCHAR NOT NULL,
    data_asset_id VARCHAR NOT NULL,
    dimension VARCHAR NOT NULL,
    value DOUBLE NOT NULL,
    observed_at TIMESTAMP NOT NULL,
    available_at TIMESTAMP NOT NULL,
    recorded_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS governance.governance_events (
    governance_event_id VARCHAR PRIMARY KEY,
    data_asset_id VARCHAR NOT NULL,
    event_type VARCHAR NOT NULL,
    occurred_at TIMESTAMP NOT NULL,
    available_at TIMESTAMP NOT NULL,
    severity VARCHAR NOT NULL,
    status VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    recorded_at TIMESTAMP NOT NULL
);
"""
