# RiskSignal

## AI Powered Risk Intelligence

RiskSignal is a synthetic enterprise risk intelligence platform designed to detect noteworthy changes, identify meaningful patterns, surface signals, preserve the evidence supporting them, and provide explainable investigation and recommendations.

RiskSignal is **domain neutral by design**. Data Governance is the first implemented domain, but the architecture is intended to support broader technology, cybersecurity, AI, operational, financial, market, and other risk intelligence use cases.

The platform combines:

* Deterministic detection and pattern recognition
* Point in time context and temporal integrity
* Evidence based signals
* Significance assessment
* Closed world AI investigation
* Deterministic validation and recommendations
* Explicit human decision making

The goal is not to build a black box that predicts risk.

The goal is to build a system that can answer:

> **What changed, what pattern does it represent, what evidence supports it, how significant is it, what might explain it, and what should a human consider next?**

---

## Why RiskSignal?

Enterprise risk rarely appears as a single obvious event.

It often emerges through relationships between:

* Data quality measurements
* Ownership and accountability
* Business entities
* Technology assets
* Process events
* Historical trends
* Control activity
* Changes over time

Traditional reporting often shows these facts separately.

RiskSignal is designed to connect them.

The intelligence flow is:

**Understand context → Detect noteworthy changes → Identify patterns → Generate signals → Collect evidence → Determine significance → Investigate → Recommend → Human decision**

A useful mental model is:

> **Triggers are what RiskSignal notices. Patterns are what RiskSignal understands. Signals are what RiskSignal surfaces. Significance describes how much attention the signal warrants.**

---

## Core Architecture

```text
                              DOMAIN DATA
                                  │
                                  ▼
                           Domain Adapter
                                  │
                                  ▼
                        Canonical Projection
                                  │
                                  ▼
                           Context Engine
                                  │
                                  ▼
                         Detection Engine
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                           ▼
             Trigger Detection           Pattern Detection
                    │                           │
                    └─────────────┬─────────────┘
                                  ▼
                           Signal Generation
                                  │
                                  ▼
                         Evidence Collection
                                  │
                                  ▼
                       Significance Assessment
                                  │
                                  ▼
                         Evidence Package
                         ┌────────┴────────┐
                         │                 │
                         ▼                 ▼
                  Deterministic       AI Investigation
                  Investigation             │
                         │                  ▼
                         │             AI Validation
                         │                  │
                         └────────┬─────────┘
                                  ▼
                           Recommendation
                                  │
                                  ▼
                            Human Decision
```

The Detection Engine contains both trigger detection and pattern detection.

AI does not determine whether a signal exists. It receives a deterministic evidence package after the signal has already been generated.

---

## Core Pipeline Summary

| Stage                   | Mechanism       | Primary Responsibility                                                                     |
| ----------------------- | --------------- | ------------------------------------------------------------------------------------------ |
| Context Engine          | Deterministic   | Builds point in time context from valid observations, relationships, and events            |
| Detection Engine        | Deterministic   | Identifies noteworthy triggers and meaningful patterns                                     |
| Signal Generation       | Deterministic   | Converts detected patterns into formal RiskSignal outputs                                  |
| Evidence Builder        | Deterministic   | Assembles constitutive and contextual evidence available at the evaluation time            |
| Significance Assessment | Deterministic   | Determines the attention level warranted by the signal                                     |
| AI Investigator         | Closed World AI | Interprets the supplied evidence package without accessing unrestricted data               |
| Validation Layer        | Deterministic   | Checks AI output for grounding, valid evidence references, structure, and supported claims |
| Recommendation          | Deterministic   | Produces the canonical recommendation from the signal and evidence                         |
| Human Decision          | Human           | Makes the final decision                                                                   |

The deterministic layers establish **what RiskSignal knows**.

The AI layer helps interpret **what that evidence may mean**.

The human remains responsible for the final decision.

---

# Trigger, Pattern, Signal, Significance

These concepts are intentionally separate.

## Trigger

A **Trigger** is a noteworthy deviation from expected behavior.

It may represent:

* A sudden change
* An unexpected measurement
* A threshold crossing
* A relationship becoming inactive
* A control condition changing

A trigger does not automatically become a pattern or a signal.

Triggers are an intelligence concept inside the Detection Engine rather than a canonical data object.

### Example

A data asset's timeliness changes from 98 to 91.

RiskSignal may notice:

> Timeliness deteriorated unexpectedly.

That is a trigger.

---

## Pattern

A **Pattern** is a meaningful relationship, trend, or condition identified from one or more observations, triggers, relationships, or events.

Examples include:

* Consecutive metric decline
* Missing required relationship
* Ownership vacancy
* Compound conditions involving different indicator families

A pattern represents something RiskSignal has interpreted from the available context.

### Example

Timeliness changes:

```text
98 → 94 → 89
```

The repeated deterioration forms a:

> `consecutive_metric_decline`

pattern.

---

## Signal

A **Signal** is a formal RiskSignal output generated from a detected pattern.

Not every noteworthy observation or pattern necessarily needs to become a signal.

Signals provide a structured way to surface meaningful conditions for investigation, monitoring, or decision making.

Examples include:

* `emerging_deterioration`
* `missing_relationship`
* `compound_risk`

A signal is **not automatically a confirmed risk**.

It is a structured indication that something warrants attention.

---

## Significance

Significance describes **how much attention a signal warrants**.

The current conceptual model uses four levels:

| Level           | Meaning                                                |
| --------------- | ------------------------------------------------------ |
| **DETECTED**    | RiskSignal has detected a trigger or noteworthy change |
| **EMERGING**    | A meaningful pattern is emerging                       |
| **INVESTIGATE** | The signal warrants prioritized investigation          |
| **ATTENTION**   | Leadership involvement should be prioritized now       |

These levels describe significance, not response.

A signal at an earlier level may still lead to monitoring, communication, review, or action.

Similarly, a higher significance level does not prescribe the final business response.

Response remains a separate decision.

---

# Domain Neutral Design

RiskSignal separates the **platform intelligence model** from the **domain specific data model**.

The platform does not assume that risk comes from a particular type of data.

Instead:

```text
Domain Data
     │
     ▼
Domain Adapter
     │
     ▼
Canonical Model
     │
     ▼
Domain Neutral Intelligence
```

This allows different domains to provide their own entities, relationships, observations, and events while using the same downstream intelligence architecture.

Data Governance is currently the first domain adapter.

Future adapters could support areas such as:

* Technology Risk
* Cybersecurity Risk
* AI Risk
* Operational Risk
* Financial Risk
* Market Intelligence
* Business Operations
* Supply Chain Risk

The same core concepts remain:

**Context → Detection → Patterns → Signals → Evidence → Significance → Investigation → Recommendation → Decision**

---

# Canonical Model

RiskSignal uses a canonical model as a common language between domain data and the intelligence engines.

The current canonical model contains ten objects:

```text
Entity
Relationship
Observation
Event
Pattern
Signal
Evidence
Investigation
Recommendation
Decision
```

## Entity

Something that exists in the domain.

Examples:

* Data asset
* Business unit
* Employee
* Application
* Technology service
* Customer
* Security control

---

## Relationship

A connection between entities.

Examples:

* Owns
* Stewards
* Supports
* Depends on
* Reports to
* Controls

Relationships can have their own temporal validity.

---

## Observation

A measured or observed value at a point in time.

Examples:

* Timeliness = 91
* Completeness = 98
* Accuracy = 94
* Duplicate rate = 2%

Observations are time bearing and cannot be used before they are available to the system.

---

## Event

Something that occurred.

Examples:

* Migration
* Ownership change
* Control change
* Organizational change
* Incident
* Certification event

Events provide context rather than automatically proving causality.

---

## Pattern

A meaningful relationship or condition detected from canonical context.

Examples:

* Consecutive metric decline
* Missing relationship
* Compound pattern

---

## Signal

A formal output generated from a detected pattern.

A signal captures the condition that RiskSignal wants to surface for investigation or attention.

---

## Evidence

A specific piece of information supporting a pattern, signal, or investigation.

Evidence is divided into:

**Constitutive evidence**

Evidence that explains why the signal or pattern exists.

**Contextual evidence**

Evidence that helps explain or investigate the condition but does not independently establish why the signal fired.

This distinction is important for explainability.

---

## Investigation

A structured interpretation of a signal and its evidence.

RiskSignal can support both:

* Deterministic investigation
* AI assisted investigation

AI investigation is constrained by a closed evidence package and validated before being presented as part of the intelligence workflow.

---

## Recommendation

A deterministic recommendation generated from the signal and evidence.

The AI investigator may provide suggested next steps, but it does not replace the canonical deterministic recommendation.

---

## Decision

The final human decision.

RiskSignal does not attempt to automate the human decision.

---

# Temporal Integrity

Temporal correctness is a first class design principle.

RiskSignal distinguishes between:

* When something occurred
* When something was observed
* When information became available to the system

For example:

```text
occurred_at
observed_at
available_at
detected_at
```

An evaluation performed at:

```text
as_of = 2026-01-15
```

must not use information that only became available after that point.

This prevents future information from leaking into historical detection.

The rule is:

> **If information was not available at the evaluation time, the intelligence engine cannot use it.**

This applies to observations, events, relationships, evidence, patterns, and downstream investigation.

---

# Data Governance Vertical Slice

The first implemented domain is Data Governance.

The current synthetic data model includes:

```text
business_units
employees
data_assets
data_asset_ownership
dq_rules
dq_measurements
governance_events
```

The initial vertical slice centers on data asset:

```text
DA047 — Credit Exposure Amount
```

The synthetic scenario includes:

* Deteriorating timeliness
* Data quality measurements
* Ownership relationships
* A migration event
* Historical context
* A future measurement that must not leak into earlier analysis

The current Data Quality Score uses:

```text
30% Completeness
30% Accuracy
20% Timeliness
20% Uniqueness
```

Where:

```text
Uniqueness = 100 − Duplicate Rate
```

The purpose of the synthetic data is not to simulate a production environment.

It exists to provide controlled scenarios where the intelligence system can be tested against known conditions.

---

# Deterministic Intelligence

The current deterministic intelligence layer includes several reusable patterns.

## Consecutive Metric Decline

Detects repeated deterioration in a metric.

The detector is domain neutral.

It can potentially apply to:

* Data quality
* System availability
* Security metrics
* Processing latency
* Financial indicators
* Operational metrics

The same pattern structure can therefore be reused across domains.

---

## Missing Relationship

Detects when a required relationship is absent or inactive.

For example:

```text
Data Asset
    │
    └── Owner → inactive
```

A steward relationship may still exist, but the required accountable owner relationship is missing.

The pattern detector evaluates the relationship at the requested point in time.

---

## Compound Pattern

Combines independent indicator families.

For example:

```text
Consecutive Metric Decline
             +
Missing Accountability
             │
             ▼
       Compound Pattern
```

The current implementation intentionally avoids treating multiple correlated measurements as independent evidence merely because they deteriorate together.

For example:

```text
Timeliness decline
        +
DQ score decline
```

may represent related manifestations of the same underlying condition rather than two independent risk indicators.

Future versions can introduce validated composite discovery rather than manually creating large numbers of combinations.

---

# Evidence

Evidence is constructed deterministically.

For every signal, RiskSignal distinguishes between:

### Constitutive evidence

Evidence that directly supports why the pattern or signal was generated.

Examples:

* Supporting observations
* Detected patterns
* Expired relationships
* Missing required relationships

### Contextual evidence

Evidence that may help explain the condition.

Examples:

* Migration events
* Related relationships
* Organizational changes

Contextual evidence cannot be promoted into proof merely because it provides a plausible explanation.

For example, a migration event may provide a possible explanation for deteriorating timeliness.

It does not, by itself, prove that the migration caused the deterioration.

---

# Closed World AI Investigation

AI enters the architecture **after deterministic evidence construction**.

```text
Signal
   │
   ▼
Evidence
   │
   ▼
Evidence Package
   │
   ▼
AI Investigator
   │
   ▼
Validation
   │
   ▼
Investigation
```

The AI investigator receives a bounded evidence package.

It does not have unrestricted access to the underlying data.

The evidence package contains:

* Evaluation timestamp
* Subject entity
* Signal metadata
* Pattern metadata
* Constitutive evidence
* Contextual evidence

This creates a **closed world investigation boundary**.

The AI can interpret the supplied evidence, but it cannot independently retrieve additional facts from the wider system.

---

# AI Investigation Contract

The AI layer is intentionally separated from model providers.

The current interfaces include:

```text
EvidencePackageBuilder
Investigator
InvestigationValidator
```

The investigator returns a structured result containing:

```text
summary
findings
supporting_evidence_ids
possible_explanations
unknowns
recommended_next_steps
confidence
```

This allows the intelligence architecture to remain independent of a particular model, vendor, SDK, or deployment environment.

A future implementation could use:

* A local LLM
* A hosted model
* An enterprise model
* Another provider implementing the same contract

The core architecture does not change.

---

# AI Validation

LLM output is treated as untrusted until validated.

The validation layer checks for issues such as:

* Missing required fields
* Invalid confidence values
* Duplicate evidence identifiers
* Evidence identifiers that do not exist
* Findings without supporting evidence
* Claims that are not grounded in the supplied evidence
* Invalid output structure

The intended flow is:

```text
AI Investigator
      │
      ▼
InvestigationResult
      │
      ▼
Deterministic Validator
      │
   ┌──┴──┐
   ▼     ▼
 Valid  Invalid
   │      │
   ▼      ▼
Use AI   Discard AI result
result    and preserve
          deterministic path
```

RiskSignal therefore fails closed.

A validation failure does not change the signal and does not replace the deterministic investigation or recommendation.

---

# Recommendation

Recommendations remain deterministic.

For example, a compound condition involving deteriorating quality and missing accountability may result in recommendations such as:

* Restore the required active relationship
* Increase monitoring
* Validate relevant control activity
* Prioritize investigation of upstream processing stability when contextual evidence indicates a migration

The AI investigator may suggest next steps.

Those suggestions are supplementary.

The canonical recommendation remains deterministic.

---

# Human Decision

RiskSignal does not attempt to make the final decision.

The intended flow is:

```text
Detection
    ↓
Pattern
    ↓
Signal
    ↓
Evidence
    ↓
Significance
    ↓
Investigation
    ↓
Recommendation
    ↓
Human Decision
```

The system provides structured intelligence.

The human decides what to do with it.

---

# Current Implementation

The current repository contains a working deterministic intelligence vertical slice and the initial AI boundary.

Implemented today:

* Domain adapter architecture
* Canonical model
* Point in time context
* Temporal relationship evaluation
* Trigger concepts within detection
* Consecutive metric decline detection
* Missing relationship detection
* Compound pattern composition
* Signal generation
* Constitutive and contextual evidence
* Deterministic investigation
* Deterministic recommendations
* Closed world evidence package
* AI investigation contract
* AI validation contract
* Unit and integration tests

The live LLM is **not yet connected**.

The current AI implementation establishes the architecture and contracts before introducing a model dependency.

---

# AI Foundation

The initial AI foundation includes:

```text
EvidencePackage
EvidencePackageBuilder
Investigator
InvestigationResult
InvestigationValidator
ValidationReport
```

The current implementation includes a deterministic evidence package builder.

This allows the AI boundary to be tested independently of any model provider.

The next milestone is a non networked investigator implementation that can exercise the complete contract and validation flow before introducing a local LLM.

---

# Testing

RiskSignal uses synthetic scenarios and automated tests to validate deterministic behavior.

The current test suite covers:

* Canonical models
* Domain mapping
* Temporal behavior
* Pattern detection
* Relationship conditions
* Compound patterns
* Signal generation
* Evidence construction
* End to end DA047 behavior
* Closed world AI evidence packages
* Constitutive versus contextual evidence

Current status:

```text
18 tests passing
```

A key testing principle is that future information must never appear in historical analysis.

For example, a future measurement for DA047 must remain invisible when evaluating an earlier `as_of` timestamp.

---

# What Comes Next

The next development stages are intentionally focused on intelligence rather than infrastructure.

## 1. AI Investigation

Implement a non networked investigator against the existing contract.

## 2. AI Validation

Complete deterministic validation of structured investigation results.

## 3. Local LLM

Connect a locally running model to the investigator interface.

The first goal is not model sophistication.

It is proving that a real model can operate safely inside the closed world evidence boundary.

## 4. Tool Calling

Allow controlled investigation tools where appropriate.

Any future tool access should remain constrained by explicit permissions and evidence boundaries.

## 5. Evaluation

Build repeatable evaluation scenarios covering:

* Grounded findings
* Unsupported claims
* Unknown evidence IDs
* Missing evidence
* Temporal leakage
* Contradictory evidence
* Confidence behavior
* Recommendation alignment

The goal is to measure whether AI improves investigation quality without weakening determinism or explainability.

---

# Future Intelligence

The current MVP uses deterministic patterns.

The longer term direction is not to manually create every possible combination of signals.

A future intelligence layer could discover and validate composite relationships from historical or synthetic scenarios.

For example:

```text
Indicator A
     +
Indicator B
     +
Context C
     │
     ▼
Candidate Composite
     │
     ▼
Statistical / Historical Validation
     │
     ▼
Validated Composite Pattern
```

Only combinations that demonstrate useful and repeatable behavior would be promoted into the intelligence layer.

This provides a path from deterministic pattern detection toward validated pattern discovery without turning the platform into an arbitrary scoring engine.

---

# Future Domains and Use Cases

Because the architecture is domain neutral, the same intelligence framework can eventually be applied to other types of structured signals.

Potential domains include:

### Technology Risk

* Technology asset degradation
* Control gaps
* Unsupported technology
* Ownership changes
* Repeated operational exceptions

### Cybersecurity

* Security control deterioration
* Vulnerability trends
* Control ownership gaps
* Repeated incidents
* Correlated security indicators

### AI Risk

* AI system control gaps
* Model monitoring deterioration
* Missing accountability
* Governance events
* Control effectiveness trends

### Financial and Market Intelligence

The same architecture could also analyze time series and contextual relationships in areas such as:

* Stocks
* Crypto assets
* Market indicators
* Trading activity
* Corporate events

The domain adapter would translate domain specific data into the canonical model.

The downstream intelligence architecture would remain substantially the same:

```text
Domain Data
    ↓
Canonical Projection
    ↓
Context
    ↓
Detection
    ↓
Patterns
    ↓
Signals
    ↓
Evidence
    ↓
Significance
    ↓
Investigation
    ↓
Recommendation
```

---

# Technology Stack

The project intentionally uses a lightweight local stack.

Current technologies include:

* Python
* Pandas
* SQL
* DuckDB
* Synthetic enterprise data
* Python dataclasses and protocols
* Pytest
* Visualization tooling as needed

Future AI experimentation may include:

* Local LLMs
* Tool calling
* Structured model outputs
* Evaluation frameworks

The architecture deliberately avoids unnecessary infrastructure.

There is currently no requirement for:

* Cloud infrastructure
* Kubernetes
* Microservices
* Postgres
* Vector databases
* Production APIs
* Agent frameworks

The objective is to spend more effort on intelligence, scenarios, evaluation, explainability, and AI behavior than on infrastructure.

---

# Development Philosophy

RiskSignal follows several principles.

### Determinism before AI

The system should establish what happened before asking AI to interpret it.

### Evidence before narrative

Every investigation should be grounded in explicit evidence.

### Temporal correctness

Historical analysis must not use information that was unavailable at the evaluation time.

### Closed world AI

AI should operate within a controlled evidence boundary.

### Fail closed

If AI output cannot be validated, the deterministic path remains authoritative.

### Human decision

The system informs decisions rather than making them.

### Domain neutrality

Domain specific logic belongs in adapters rather than the platform core.

### Intelligence over infrastructure

Infrastructure should support the intelligence rather than become the project.

---

# Repository Structure

```text
RiskSignal/
│
├── src/
│   └── risksignal/
│       ├── canonical/
│       │   └── models.py
│       │
│       ├── domains/
│       │   └── data_governance/
│       │
│       ├── intelligence/
│       │   ├── ai/
│       │   │   ├── contracts.py
│       │   │   ├── package.py
│       │   │   └── __init__.py
│       │   │
│       │   ├── context.py
│       │   ├── evidence.py
│       │   ├── investigation.py
│       │   ├── pattern.py
│       │   ├── recommendation.py
│       │   ├── signal.py
│       │   └── stages.py
│       │
│       └── pipeline.py
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── notebooks/
│
├── pyproject.toml
└── README.md
```

---

# Running the Project

Install the project with development dependencies:

```bash
pip install -e ".[dev]"
```

Run the test suite:

```bash
pytest
```

The repository currently uses the test suite as the primary executable verification of the intelligence pipeline.

A dedicated demonstration command can be added later once the pipeline interface is intentionally exposed as a stable CLI.

---

# Project Status

**Current stage: Deterministic Intelligence + AI Foundation**

Implemented:

```text
Domain Adapter
      ↓
Canonical Projection
      ↓
Temporal Context
      ↓
Detection
      ↓
Triggers
      ↓
Patterns
      ↓
Signals
      ↓
Evidence
      ↓
Significance Model
      ↓
Evidence Package
```

The deterministic investigation and recommendation path is implemented.

The AI boundary and evidence package contract are implemented.

The next step is to connect a non networked investigator, validate the AI contract, and then introduce a local LLM.

The significance model is currently defined conceptually as a distinct assessment layer and will be implemented independently of AI.

---

# Disclaimer

RiskSignal is an independent personal project using synthetic data.

It does not use employer confidential information, production data, proprietary datasets, or confidential business logic.

The project is intended to demonstrate concepts in:

* Data Governance
* Risk Intelligence
* Data and Analytics
* AI assisted investigation
* Explainable intelligence
* Temporal reasoning
* Evidence based decision support
* Domain neutral architecture
