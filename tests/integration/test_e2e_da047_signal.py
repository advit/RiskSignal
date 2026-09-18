from risksignal.adapters.data_governance.seed import ASSET_ID, build_seed, demo_as_of
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
