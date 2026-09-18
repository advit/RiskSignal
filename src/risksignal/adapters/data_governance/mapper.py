from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from risksignal.adapters.data_governance.models import (
    BusinessUnit,
    DataAsset,
    DataAssetOwnership,
    DqMeasurement,
    DqRule,
    Employee,
    GovernanceEvent,
)
from risksignal.canonical.models import Entity, Event, Observation, Relationship

SOURCE = "data_governance"

COMPOSITE_WEIGHTS = {
    "completeness": 0.30,
    "accuracy": 0.30,
    "timeliness": 0.20,
    "uniqueness": 0.20,
}


@dataclass(frozen=True)
class CanonicalProjection:
    entities: list[Entity]
    relationships: list[Relationship]
    observations: list[Observation]
    events: list[Event]


def _entity(
    entity_id: str,
    entity_type: str,
    name: str,
    source_id: str,
    **attributes: object,
) -> Entity:
    return Entity(
        entity_id=entity_id,
        entity_type=entity_type,
        name=name,
        source_system=SOURCE,
        source_id=source_id,
        attributes=dict(attributes),
    )


def project(
    *,
    business_units: list[BusinessUnit],
    employees: list[Employee],
    data_assets: list[DataAsset],
    ownership: list[DataAssetOwnership],
    dq_rules: list[DqRule],
    dq_measurements: list[DqMeasurement],
    governance_events: list[GovernanceEvent],
) -> CanonicalProjection:
    entities: list[Entity] = []
    relationships: list[Relationship] = []
    observations: list[Observation] = []
    events: list[Event] = []

    for unit in business_units:
        entities.append(
            _entity(
                f"bu:{unit.business_unit_id}",
                "business_unit",
                unit.name,
                unit.business_unit_id,
                function=unit.function,
            )
        )
        if unit.parent_business_unit_id:
            relationships.append(
                Relationship(
                    relationship_id=f"rel:bu-parent:{unit.business_unit_id}",
                    from_entity_id=f"bu:{unit.business_unit_id}",
                    to_entity_id=f"bu:{unit.parent_business_unit_id}",
                    relationship_type="child_of",
                    available_at=_epoch(),
                    source_system=SOURCE,
                    source_id=unit.business_unit_id,
                )
            )

    for employee in employees:
        entities.append(
            _entity(
                f"emp:{employee.employee_id}",
                "employee",
                employee.full_name,
                employee.employee_id,
                role_title=employee.role_title,
                line=employee.line,
            )
        )
        relationships.append(
            Relationship(
                relationship_id=f"rel:emp-bu:{employee.employee_id}",
                from_entity_id=f"emp:{employee.employee_id}",
                to_entity_id=f"bu:{employee.business_unit_id}",
                relationship_type="member_of",
                available_at=_epoch(),
                source_system=SOURCE,
                source_id=employee.employee_id,
            )
        )

    for asset in data_assets:
        entities.append(
            _entity(
                f"asset:{asset.data_asset_id}",
                "data_asset",
                asset.name,
                asset.data_asset_id,
                criticality=asset.criticality,
                lifecycle_state=asset.lifecycle_state,
                is_authoritative_source=asset.is_authoritative_source,
                description=asset.description,
            )
        )
        relationships.append(
            Relationship(
                relationship_id=f"rel:asset-bu:{asset.data_asset_id}",
                from_entity_id=f"asset:{asset.data_asset_id}",
                to_entity_id=f"bu:{asset.business_unit_id}",
                relationship_type="owned_by_unit",
                available_at=_epoch(),
                source_system=SOURCE,
                source_id=asset.data_asset_id,
            )
        )

    for item in ownership:
        relationships.append(
            Relationship(
                relationship_id=f"rel:own:{item.ownership_id}",
                from_entity_id=f"emp:{item.employee_id}",
                to_entity_id=f"asset:{item.data_asset_id}",
                relationship_type=item.ownership_role,
                available_at=item.available_at,
                valid_from=item.effective_from,
                valid_to=item.effective_to,
                source_system=SOURCE,
                source_id=item.ownership_id,
            )
        )

    for rule in dq_rules:
        entities.append(
            _entity(
                f"rule:{rule.dq_rule_id}",
                "dq_rule",
                rule.name,
                rule.dq_rule_id,
                dimension=rule.dimension,
                threshold=rule.threshold,
                weight=rule.weight,
            )
        )
        relationships.append(
            Relationship(
                relationship_id=f"rel:rule-asset:{rule.dq_rule_id}",
                from_entity_id=f"rule:{rule.dq_rule_id}",
                to_entity_id=f"asset:{rule.data_asset_id}",
                relationship_type="applies_to",
                available_at=_epoch(),
                source_system=SOURCE,
                source_id=rule.dq_rule_id,
            )
        )

    for measurement in dq_measurements:
        observations.append(
            Observation(
                observation_id=f"obs:{measurement.dq_measurement_id}",
                subject_entity_id=f"asset:{measurement.data_asset_id}",
                observation_type="dq_measurement",
                metric_name=measurement.dimension,
                value=measurement.value,
                observed_at=measurement.observed_at,
                available_at=measurement.available_at,
                source_system=SOURCE,
                source_id=measurement.dq_measurement_id,
                attributes={"dq_rule_id": measurement.dq_rule_id},
            )
        )

    observations.extend(_composite_scores(dq_measurements))

    for event in governance_events:
        events.append(
            Event(
                event_id=f"evt:{event.governance_event_id}",
                subject_entity_id=f"asset:{event.data_asset_id}",
                event_type=event.event_type,
                occurred_at=event.occurred_at,
                available_at=event.available_at,
                source_system=SOURCE,
                source_id=event.governance_event_id,
                payload={
                    "severity": event.severity,
                    "status": event.status,
                    "description": event.description,
                },
            )
        )

    return CanonicalProjection(
        entities=entities,
        relationships=relationships,
        observations=observations,
        events=events,
    )


def _composite_scores(measurements: list[DqMeasurement]) -> list[Observation]:
    grouped: dict[tuple[str, datetime], dict[str, DqMeasurement]] = {}
    for measurement in measurements:
        key = (measurement.data_asset_id, measurement.observed_at)
        grouped.setdefault(key, {})[measurement.dimension] = measurement

    composites: list[Observation] = []
    for (asset_id, observed_at), by_dim in grouped.items():
        if set(COMPOSITE_WEIGHTS) - set(by_dim):
            continue
        completeness = by_dim["completeness"].value
        accuracy = by_dim["accuracy"].value
        timeliness = by_dim["timeliness"].value
        uniqueness = by_dim["uniqueness"].value
        score = (
            COMPOSITE_WEIGHTS["completeness"] * completeness
            + COMPOSITE_WEIGHTS["accuracy"] * accuracy
            + COMPOSITE_WEIGHTS["timeliness"] * timeliness
            + COMPOSITE_WEIGHTS["uniqueness"] * uniqueness
        )
        available_at = max(item.available_at for item in by_dim.values())
        composites.append(
            Observation(
                observation_id=f"obs:composite:{asset_id}:{observed_at.date().isoformat()}",
                subject_entity_id=f"asset:{asset_id}",
                observation_type="composite_score",
                metric_name="dq_score",
                value=round(score, 4),
                observed_at=observed_at,
                available_at=available_at,
                source_system=SOURCE,
                source_id=f"composite:{asset_id}:{observed_at.date().isoformat()}",
                attributes={"formula": "weighted_dq_dimensions"},
            )
        )
    return composites


def _epoch() -> datetime:
    return datetime(1970, 1, 1)
