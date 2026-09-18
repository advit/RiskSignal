from datetime import datetime, timedelta

from risksignal.canonical.models import Entity, Observation, Relationship


def test_entity_is_domain_neutral():
    entity = Entity(
        entity_id="e1",
        entity_type="anything",
        name="Example",
        source_system="test",
        source_id="1",
        attributes={"criticality": "critical"},
    )
    assert entity.entity_type == "anything"
    assert "dq_" not in entity.__dataclass_fields__


def test_observation_eligibility_uses_available_at_not_observed_at():
    as_of = datetime(2026, 1, 10, 9, 0, 0)
    eligible = Observation(
        observation_id="o1",
        subject_entity_id="e1",
        observation_type="metric",
        metric_name="timeliness",
        value=70,
        observed_at=datetime(2026, 1, 9),
        available_at=datetime(2026, 1, 10, 8, 0, 0),
        source_system="test",
        source_id="o1",
    )
    ineligible = Observation(
        observation_id="o2",
        subject_entity_id="e1",
        observation_type="metric",
        metric_name="timeliness",
        value=10,
        observed_at=datetime(2026, 1, 9),
        available_at=datetime(2026, 1, 11, 9, 0, 0),
        source_system="test",
        source_id="o2",
    )
    assert eligible.is_eligible_at(as_of)
    assert not ineligible.is_eligible_at(as_of)


def test_relationship_validity_window():
    as_of = datetime(2026, 6, 1)
    rel = Relationship(
        relationship_id="r1",
        from_entity_id="a",
        to_entity_id="b",
        relationship_type="owner",
        available_at=datetime(2026, 1, 1),
        source_system="test",
        source_id="r1",
        valid_from=datetime(2026, 1, 1),
        valid_to=datetime(2026, 3, 1),
    )
    assert not rel.is_active_at(as_of)
    assert rel.is_active_at(datetime(2026, 2, 1))
    assert rel.involves("a")
    future = Relationship(
        relationship_id="r2",
        from_entity_id="a",
        to_entity_id="b",
        relationship_type="owner",
        available_at=as_of + timedelta(days=1),
        source_system="test",
        source_id="r2",
    )
    assert not future.is_active_at(as_of)
