from risksignal.adapters.data_governance.mapper import COMPOSITE_WEIGHTS, project
from risksignal.adapters.data_governance.seed import build_seed


def test_mapper_projects_seven_governance_structures():
    seed = build_seed()
    projection = project(**seed)
    types = {entity.entity_type for entity in projection.entities}
    assert types == {"business_unit", "employee", "data_asset", "dq_rule"}
    rel_types = {rel.relationship_type for rel in projection.relationships}
    assert {"owner", "steward", "member_of", "owned_by_unit", "applies_to"} <= rel_types
    assert any(obs.metric_name == "timeliness" for obs in projection.observations)
    assert any(obs.metric_name == "dq_score" for obs in projection.observations)
    assert any(event.event_type == "migration" for event in projection.events)
    assert all(item.source_system == "data_governance" for item in projection.entities)


def test_composite_score_matches_documented_weights():
    seed = build_seed()
    projection = project(**seed)
    first_day = min(
        obs.observed_at
        for obs in projection.observations
        if obs.metric_name == "completeness"
    )
    by_name = {
        obs.metric_name: obs.value
        for obs in projection.observations
        if obs.observed_at == first_day and obs.observation_type == "dq_measurement"
    }
    composite = next(
        obs.value
        for obs in projection.observations
        if obs.metric_name == "dq_score" and obs.observed_at == first_day
    )
    expected = (
        COMPOSITE_WEIGHTS["completeness"] * by_name["completeness"]
        + COMPOSITE_WEIGHTS["accuracy"] * by_name["accuracy"]
        + COMPOSITE_WEIGHTS["timeliness"] * by_name["timeliness"]
        + COMPOSITE_WEIGHTS["uniqueness"] * by_name["uniqueness"]
    )
    assert round(composite, 4) == round(expected, 4)


def test_future_measurement_is_projected_but_marked_later_available():
    seed = build_seed()
    projection = project(**seed)
    future = next(obs for obs in projection.observations if obs.source_id == "M-TIME-FUTURE")
    latest_eligible_available = max(
        obs.available_at
        for obs in projection.observations
        if obs.source_id != "M-TIME-FUTURE" and obs.metric_name == "timeliness"
    )
    assert future.available_at > latest_eligible_available
