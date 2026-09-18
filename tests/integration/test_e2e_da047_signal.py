from dataclasses import replace
from datetime import datetime

from risksignal.adapters.data_governance.seed import ASSET_ID, build_seed, demo_as_of
from risksignal.intelligence.evidence import CONSTITUTIVE_ROLES
from risksignal.persistence.duckdb_store import DuckDBStore
from risksignal.pipeline import ingest_data_governance, record_decision, run_intelligence


def test_da047_end_to_end_explainable_signal():
    store = DuckDBStore(":memory:")
    seed = build_seed()
    ingest_data_governance(store, seed)

    tables = [
        "business_units",
        "employees",
        "data_assets",
        "data_asset_ownership",
        "dq_rules",
        "dq_measurements",
        "governance_events",
    ]
    for table in tables:
        count = store.conn.execute(f"SELECT COUNT(*) FROM governance.{table}").fetchone()[0]
        assert count > 0, table

    as_of = demo_as_of()
    result = run_intelligence(store, subject_entity_id=f"asset:{ASSET_ID}", as_of=as_of)

    assert result.patterns
    assert result.signals
    assert {signal.signal_type for signal in result.signals} == {"emerging_deterioration"}
    assert any(signal.attributes.get("metric_name") == "timeliness" for signal in result.signals)

    roles = {item.role for item in result.evidence}
    assert "supporting_observation" in roles
    assert "contextual_event" in roles
    assert "context_relationship" in roles
    assert not any("FUTURE" in item.referenced_id for item in result.evidence)
    assert all(item.available_at <= as_of for item in result.evidence)

    assert any("timeliness" in item.description for item in result.evidence)
    assert any("dq_score" in item.description for item in result.evidence)
    assert any("migration" in item.description.lower() for item in result.evidence)

    investigation = result.investigations[0]
    assert ASSET_ID in investigation.narrative or "Credit Exposure" in investigation.narrative
    assert "available_at" in investigation.narrative

    recommendation = result.recommendations[0]
    assert "migration" in recommendation.action.lower()

    decision = record_decision(
        store,
        recommendation_id=recommendation.recommendation_id,
        decided_by="EMP-001",
        decision_type="accept",
        decided_at=as_of,
        notes="Increase monitoring during migration.",
    )
    stored = store.conn.execute("SELECT COUNT(*) FROM canonical.decisions").fetchone()[0]
    assert stored == 1
    assert decision.decision_type == "accept"
    persisted_signals = store.conn.execute("SELECT COUNT(*) FROM canonical.signals").fetchone()[0]
    assert persisted_signals == len(result.signals)
    assert persisted_signals >= 1


def test_da047_compound_decline_and_missing_relationship():
    store = DuckDBStore(":memory:")
    seed = build_seed()
    seed["ownership"] = [
        replace(item, effective_to=datetime(2026, 1, 10))
        if item.ownership_role == "owner"
        else item
        for item in seed["ownership"]
    ]
    ingest_data_governance(store, seed)
    as_of = demo_as_of()
    result = run_intelligence(store, subject_entity_id=f"asset:{ASSET_ID}", as_of=as_of)

    types = {item.pattern_type for item in result.patterns}
    assert "consecutive_metric_decline" in types
    assert "missing_relationship" in types
    assert "compound" in types
    assert {signal.signal_type for signal in result.signals} >= {
        "emerging_deterioration",
        "missing_relationship",
        "compound_risk",
    }

    compound_signal = next(item for item in result.signals if item.signal_type == "compound_risk")
    compound_pattern = next(item for item in result.patterns if item.pattern_id == compound_signal.pattern_id)
    compound_evidence = [
        item for item in result.evidence if item.signal_id == compound_signal.signal_id
    ]
    constitutive = [item for item in compound_evidence if item.role in CONSTITUTIVE_ROLES]
    assert {item.role for item in constitutive} >= {
        "detected_pattern",
        "constituent_pattern",
        "supporting_observation",
        "expired_relationship",
    }
    assert any("timeliness" in item.description or "dq_score" in item.description for item in constitutive)
    assert all(item.available_at <= as_of for item in compound_evidence)
    assert not any("FUTURE" in item.referenced_id for item in compound_evidence)
    assert set(compound_pattern.attributes["component_types"]) == {
        "consecutive_metric_decline",
        "missing_relationship",
    }
    investigation = next(
        item for item in result.investigations if item.signal_id == compound_signal.signal_id
    )
    assert "Constitutive evidence" in investigation.narrative
    recommendation = next(
        item
        for item in result.recommendations
        if item.investigation_id == investigation.investigation_id
    )
    assert "relationship" in recommendation.action.lower()
