from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

import duckdb

from risksignal.canonical.models import (
    Decision,
    Entity,
    Event,
    Evidence,
    Investigation,
    Observation,
    Pattern,
    Recommendation,
    Relationship,
    Signal,
)
from risksignal.adapters.data_governance.schema import GOVERNANCE_SCHEMA_SQL
from risksignal.persistence.canonical_schema import CANONICAL_SCHEMA_SQL


def _dump(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True)


def _load(raw: str | None) -> dict[str, Any]:
    if not raw:
        return {}
    return json.loads(raw)


class DuckDBStore:
    def __init__(self, path: str | Path = ":memory:") -> None:
        self.path = str(path)
        if self.path not in {":memory:", ""}:
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = duckdb.connect(self.path)
        self.init_schema()

    def init_schema(self) -> None:
        self.conn.execute(GOVERNANCE_SCHEMA_SQL)
        self.conn.execute(CANONICAL_SCHEMA_SQL)

    def execute(self, sql: str, params: list[Any] | None = None) -> Any:
        if params is None:
            return self.conn.execute(sql)
        return self.conn.execute(sql, params)

    def replace_canonical(
        self,
        *,
        entities: Iterable[Entity],
        relationships: Iterable[Relationship],
        observations: Iterable[Observation],
        events: Iterable[Event],
    ) -> None:
        self.conn.execute("DELETE FROM canonical.entities")
        self.conn.execute("DELETE FROM canonical.relationships")
        self.conn.execute("DELETE FROM canonical.observations")
        self.conn.execute("DELETE FROM canonical.events")
        for entity in entities:
            self.conn.execute(
                """
                INSERT INTO canonical.entities
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                [
                    entity.entity_id,
                    entity.entity_type,
                    entity.name,
                    _dump(entity.attributes),
                    entity.source_system,
                    entity.source_id,
                ],
            )
        for rel in relationships:
            self.conn.execute(
                """
                INSERT INTO canonical.relationships
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    rel.relationship_id,
                    rel.from_entity_id,
                    rel.to_entity_id,
                    rel.relationship_type,
                    rel.available_at,
                    rel.valid_from,
                    rel.valid_to,
                    _dump(rel.attributes),
                    rel.source_system,
                    rel.source_id,
                ],
            )
        for obs in observations:
            self.conn.execute(
                """
                INSERT INTO canonical.observations
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    obs.observation_id,
                    obs.subject_entity_id,
                    obs.observation_type,
                    obs.metric_name,
                    obs.value,
                    obs.observed_at,
                    obs.available_at,
                    _dump(obs.attributes),
                    obs.source_system,
                    obs.source_id,
                ],
            )
        for event in events:
            self.conn.execute(
                """
                INSERT INTO canonical.events
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    event.event_id,
                    event.subject_entity_id,
                    event.event_type,
                    event.occurred_at,
                    event.available_at,
                    _dump(event.payload),
                    event.source_system,
                    event.source_id,
                ],
            )

    def _query(self, sql: str) -> tuple[list[str], list[Any]]:
        result = self.conn.execute(sql)
        cols = [c[0] for c in result.description]
        return cols, result.fetchall()

    def load_entities(self) -> list[Entity]:
        cols, rows = self._query("SELECT * FROM canonical.entities")
        return [
            Entity(
                entity_id=row[cols.index("entity_id")],
                entity_type=row[cols.index("entity_type")],
                name=row[cols.index("name")],
                attributes=_load(row[cols.index("attributes")]),
                source_system=row[cols.index("source_system")],
                source_id=row[cols.index("source_id")],
            )
            for row in rows
        ]

    def load_relationships(self) -> list[Relationship]:
        cols, rows = self._query("SELECT * FROM canonical.relationships")
        return [
            Relationship(
                relationship_id=row[cols.index("relationship_id")],
                from_entity_id=row[cols.index("from_entity_id")],
                to_entity_id=row[cols.index("to_entity_id")],
                relationship_type=row[cols.index("relationship_type")],
                available_at=row[cols.index("available_at")],
                valid_from=row[cols.index("valid_from")],
                valid_to=row[cols.index("valid_to")],
                attributes=_load(row[cols.index("attributes")]),
                source_system=row[cols.index("source_system")],
                source_id=row[cols.index("source_id")],
            )
            for row in rows
        ]

    def load_observations(self) -> list[Observation]:
        cols, rows = self._query("SELECT * FROM canonical.observations")
        return [
            Observation(
                observation_id=row[cols.index("observation_id")],
                subject_entity_id=row[cols.index("subject_entity_id")],
                observation_type=row[cols.index("observation_type")],
                metric_name=row[cols.index("metric_name")],
                value=float(row[cols.index("value")]),
                observed_at=row[cols.index("observed_at")],
                available_at=row[cols.index("available_at")],
                attributes=_load(row[cols.index("attributes")]),
                source_system=row[cols.index("source_system")],
                source_id=row[cols.index("source_id")],
            )
            for row in rows
        ]

    def load_events(self) -> list[Event]:
        cols, rows = self._query("SELECT * FROM canonical.events")
        return [
            Event(
                event_id=row[cols.index("event_id")],
                subject_entity_id=row[cols.index("subject_entity_id")],
                event_type=row[cols.index("event_type")],
                occurred_at=row[cols.index("occurred_at")],
                available_at=row[cols.index("available_at")],
                payload=_load(row[cols.index("payload")]),
                source_system=row[cols.index("source_system")],
                source_id=row[cols.index("source_id")],
            )
            for row in rows
        ]

    def save_pattern(self, pattern: Pattern) -> None:
        self.conn.execute(
            """
            INSERT OR REPLACE INTO canonical.patterns
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                pattern.pattern_id,
                pattern.pattern_type,
                pattern.subject_entity_id,
                pattern.detected_at,
                pattern.as_of,
                pattern.window_start,
                pattern.window_end,
                _dump(pattern.attributes),
            ],
        )

    def save_signal(self, signal: Signal) -> None:
        self.conn.execute(
            """
            INSERT OR REPLACE INTO canonical.signals
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                signal.signal_id,
                signal.subject_entity_id,
                signal.signal_type,
                signal.severity,
                signal.detected_at,
                signal.as_of,
                signal.pattern_id,
                signal.summary,
                _dump(signal.attributes),
            ],
        )

    def save_evidence(self, items: Iterable[Evidence]) -> None:
        for item in items:
            self.conn.execute(
                """
                INSERT OR REPLACE INTO canonical.evidence
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    item.evidence_id,
                    item.signal_id,
                    item.referenced_object_type,
                    item.referenced_id,
                    item.role,
                    item.description,
                    item.available_at,
                ],
            )

    def save_investigation(self, investigation: Investigation) -> None:
        self.conn.execute(
            """
            INSERT OR REPLACE INTO canonical.investigations
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                investigation.investigation_id,
                investigation.signal_id,
                investigation.narrative,
                investigation.created_at,
                investigation.as_of,
            ],
        )

    def save_recommendation(self, recommendation: Recommendation) -> None:
        self.conn.execute(
            """
            INSERT OR REPLACE INTO canonical.recommendations
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                recommendation.recommendation_id,
                recommendation.investigation_id,
                recommendation.action,
                recommendation.rationale,
                recommendation.created_at,
            ],
        )

    def save_decision(self, decision: Decision) -> None:
        self.conn.execute(
            """
            INSERT OR REPLACE INTO canonical.decisions
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                decision.decision_id,
                decision.recommendation_id,
                decision.decided_by,
                decision.decision_type,
                decision.decided_at,
                decision.notes,
            ],
        )

    def close(self) -> None:
        self.conn.close()
