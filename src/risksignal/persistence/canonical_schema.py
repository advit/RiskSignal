"""Canonical persistence DDL."""

CANONICAL_SCHEMA_SQL = """
CREATE SCHEMA IF NOT EXISTS canonical;

CREATE TABLE IF NOT EXISTS canonical.entities (
    entity_id VARCHAR PRIMARY KEY,
    entity_type VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
    attributes VARCHAR NOT NULL,
    source_system VARCHAR NOT NULL,
    source_id VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS canonical.relationships (
    relationship_id VARCHAR PRIMARY KEY,
    from_entity_id VARCHAR NOT NULL,
    to_entity_id VARCHAR NOT NULL,
    relationship_type VARCHAR NOT NULL,
    available_at TIMESTAMP NOT NULL,
    valid_from TIMESTAMP,
    valid_to TIMESTAMP,
    attributes VARCHAR NOT NULL,
    source_system VARCHAR NOT NULL,
    source_id VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS canonical.observations (
    observation_id VARCHAR PRIMARY KEY,
    subject_entity_id VARCHAR NOT NULL,
    observation_type VARCHAR NOT NULL,
    metric_name VARCHAR NOT NULL,
    value DOUBLE NOT NULL,
    observed_at TIMESTAMP NOT NULL,
    available_at TIMESTAMP NOT NULL,
    attributes VARCHAR NOT NULL,
    source_system VARCHAR NOT NULL,
    source_id VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS canonical.events (
    event_id VARCHAR PRIMARY KEY,
    subject_entity_id VARCHAR NOT NULL,
    event_type VARCHAR NOT NULL,
    occurred_at TIMESTAMP NOT NULL,
    available_at TIMESTAMP NOT NULL,
    payload VARCHAR NOT NULL,
    source_system VARCHAR NOT NULL,
    source_id VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS canonical.patterns (
    pattern_id VARCHAR PRIMARY KEY,
    pattern_type VARCHAR NOT NULL,
    subject_entity_id VARCHAR NOT NULL,
    detected_at TIMESTAMP NOT NULL,
    as_of TIMESTAMP NOT NULL,
    window_start TIMESTAMP NOT NULL,
    window_end TIMESTAMP NOT NULL,
    attributes VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS canonical.signals (
    signal_id VARCHAR PRIMARY KEY,
    subject_entity_id VARCHAR NOT NULL,
    signal_type VARCHAR NOT NULL,
    severity VARCHAR NOT NULL,
    detected_at TIMESTAMP NOT NULL,
    as_of TIMESTAMP NOT NULL,
    pattern_id VARCHAR NOT NULL,
    summary VARCHAR NOT NULL,
    attributes VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS canonical.evidence (
    evidence_id VARCHAR PRIMARY KEY,
    signal_id VARCHAR NOT NULL,
    referenced_object_type VARCHAR NOT NULL,
    referenced_id VARCHAR NOT NULL,
    role VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    available_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS canonical.investigations (
    investigation_id VARCHAR PRIMARY KEY,
    signal_id VARCHAR NOT NULL,
    narrative VARCHAR NOT NULL,
    created_at TIMESTAMP NOT NULL,
    as_of TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS canonical.recommendations (
    recommendation_id VARCHAR PRIMARY KEY,
    investigation_id VARCHAR NOT NULL,
    action VARCHAR NOT NULL,
    rationale VARCHAR NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS canonical.decisions (
    decision_id VARCHAR PRIMARY KEY,
    recommendation_id VARCHAR NOT NULL,
    decided_by VARCHAR NOT NULL,
    decision_type VARCHAR NOT NULL,
    decided_at TIMESTAMP NOT NULL,
    notes VARCHAR NOT NULL
);
"""
