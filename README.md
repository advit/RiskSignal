# RiskSignal

## AI Powered Risk Intelligence

**IN DEVELOPMENT · GROUND TRUTH VALIDATION**

RiskSignal is an independent project exploring how enterprise data and governance signals can be connected to identify situations that may warrant investigation.

The idea is simple:

**Data → Signals → Context → Evidence → Investigation → Human Decision**

A data quality issue, ownership change, control failure or operational event may not mean much on its own.

But what if several of those things are connected?

RiskSignal is an attempt to build and test that idea.

The project currently starts with **Data Governance and Data Quality**, using synthetic enterprise data. The longer term hypothesis is that the same approach could extend into Technology, Cyber, AI, Operational and other risk domains.

This is a working project, not a production risk platform.

---

# Why RiskSignal?

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

The individual warning signs often already exist.

The harder problem is connecting them early enough to understand whether they point to a broader underlying issue.

A data quality problem may appear in one dashboard.

An ownership change may exist somewhere else.

A control issue may be recorded in a governance system.

An operational event may sit in another data source.

RiskSignal explores whether these pieces can be connected into a structured, evidence based investigation.

The goal is not to build a black box that predicts risk.

The goal is to build a system that can answer:

> **What changed, what pattern does it represent, what evidence supports it, what does the evidence suggest, and what should a human consider next?**

---

# Core Principle

RiskSignal is built around a simple boundary:

> **The system establishes the evidence. AI assists the investigation. Humans decide.**

This boundary is part of the architecture, not a future design decision.

The deterministic system establishes what happened and what evidence supports the signal.

AI can help interpret that evidence, connect information, formulate hypotheses and summarise findings.

The final decision remains with a human.

---

# Architecture

The current architecture follows:

**Detect → Connect → Evidence → Investigate → Recommend → Decide**

In simple terms:

1. **Detect**
   Identify observations or events that may warrant attention.

2. **Connect**
   Identify relationships between observations, entities, events and other relevant context.

3. **Evidence**
   Establish what information supports the signal.

4. **Investigate**
   Explore what the evidence may mean.

5. **Recommend**
   Formulate possible explanations, next steps or actions.

6. **Decide**
   Leave the final decision with a human.

The current implementation focuses primarily on the deterministic foundation and the boundary between evidence and AI assisted investigation.

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

AI does not determine whether a signal exists.

It receives a deterministic evidence package after the signal has already been generated.

---

# What is implemented?

The current working slice includes:

* A domain adapter architecture
* A canonical model for entities, relationships, observations, events, patterns and signals
* Point in time context
* Temporal relationship evaluation
* Deterministic trigger and pattern detection
* Signal generation
* Constitutive and contextual evidence
* Significance assessment
* Deterministic investigation
* Deterministic recommendations
* Closed world evidence packages
* AI investigation contracts and validation boundaries
* Automated tests covering the deterministic intelligence pipeline

The first implemented domain is **Data Governance and Data Quality**.

The project currently runs locally using a lightweight Python and DuckDB based stack.

The live LLM investigation layer is not yet connected.

That is deliberate.

The goal is to establish and test the deterministic foundation before introducing model behaviour.

---

# Trigger, Pattern, Signal and Significance

These concepts are intentionally separate.

A useful mental model is:

> **Triggers are what RiskSignal notices. Patterns are what RiskSignal identifies. Signals are what RiskSignal surfaces. Significance describes how much attention the signal warrants.**

## Trigger

A **Trigger** is a noteworthy deviation from expected behaviour.

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

A **Pattern** is a meaningful relationship, trend or condition identified from one or more observations, triggers, relationships or events.

Examples include:

* Consecutive metric decline
* Missing required relationship
* Ownership vacancy
* Compound conditions involving different indicator families

A pattern represents something RiskSignal has identified from available context.

### Example

Timeliness changes:

```text
98 → 94 → 89
```

The repeated deterioration forms a:

```text
consecutive_metric_decline
```

pattern.

---

## Signal

A **Signal** is a formal RiskSignal output generated from a detected pattern.

Not every noteworthy observation or pattern needs to become a signal.

A signal is a structured indication that something warrants attention or investigation.

Examples include:

* `emerging_deterioration`
* `missing_relationship`
* `compound_risk`

A signal is **not automatically a confirmed risk**.

The distinction is important:

> **Signal ≠ Risk**

A signal tells the system that a particular combination of evidence deserves attention.

The investigation and decision come later.

---

## Significance

Significance describes **how much attention a signal warrants**.

The current conceptual model uses four levels:

| Level           | Meaning                                                |
| --------------- | ------------------------------------------------------ |
| **DETECTED**    | RiskSignal has detected a trigger or noteworthy change |
| **EMERGING**    | A meaningful pattern is emerging                       |
| **INVESTIGATE** | The signal warrants prioritised investigation          |
| **ATTENTION**   | Leadership involvement should be prioritised           |

These levels describe significance, not the final response.

A higher significance level does not automatically prescribe what the business should do.

The response remains a separate human decision.

---

# Canonical Model

RiskSignal uses a canonical model as a common language between domain data and the intelligence engines.

The current model contains:

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

## Observation

A measured or observed value at a point in time.

Examples:

* Timeliness = 91
* Completeness = 98
* Accuracy = 94
* Duplicate rate = 2%

Observations are time bearing and cannot be used before they are available to the system.

## Event

Something that occurred.

Examples:

* Migration
* Ownership change
* Control change
* Organisational change
* Incident
* Certification event

Events provide context. They do not automatically establish causality.

## Pattern

A meaningful relationship or condition identified from canonical context.

## Signal

A formal output generated from a detected pattern.

## Evidence

A specific piece of information supporting a pattern, signal or investigation.

RiskSignal distinguishes between:

**Constitutive evidence**

Evidence that helps establish why the pattern or signal exists.

**Contextual evidence**

Evidence that helps explain or investigate the condition but does not independently establish why the signal fired.

## Investigation

A structured interpretation of a signal and its evidence.

RiskSignal supports both:

* Deterministic investigation
* AI assisted investigation

## Recommendation

A structured recommendation derived from the signal and evidence.

AI may suggest possible next steps, but it does not replace the canonical deterministic recommendation.

## Decision

The final human decision.

RiskSignal does not attempt to automate this step.

---

# Temporal Integrity

Temporal correctness is a first class design principle.

RiskSignal distinguishes between:

* When something occurred
* When something was observed
* When information became available to the system
* When the intelligence evaluation was performed

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

The rule is:

> **If information was not available at the evaluation time, the intelligence engine cannot use it.**

This prevents future information from silently influencing historical analysis.

Temporal integrity applies to observations, events, relationships, evidence, patterns and downstream investigation.

---

# Data Governance Vertical Slice

The first implemented domain is Data Governance and Data Quality.

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

The initial vertical slice centres on:

```text
DA047 — Credit Exposure Amount
```

The scenario includes:

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

It provides controlled scenarios where the system can be tested against known expected outcomes.

---

# Deterministic Intelligence

The current deterministic intelligence layer includes reusable patterns.

## Consecutive Metric Decline

Detects repeated deterioration in a metric.

The detector is domain neutral and could potentially apply to:

* Data quality
* System availability
* Security metrics
* Processing latency
* Financial indicators
* Operational metrics

## Missing Relationship

Detects when a required relationship is absent or inactive.

For example:

```text
Data Asset
    │
    └── Owner → inactive
```

The detector evaluates the relationship at the requested point in time.

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

The implementation deliberately avoids treating multiple correlated measurements as independent evidence simply because they deteriorate together.

For example:

```text
Timeliness decline
        +
DQ score decline
```

may represent related manifestations of the same underlying condition rather than two independent indicators.

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
* Organisational changes

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

The AI investigator is intended to receive a bounded evidence package rather than unrestricted access to enterprise data.

The package can contain:

* Evaluation timestamp
* Subject entity
* Signal metadata
* Pattern metadata
* Constitutive evidence
* Contextual evidence

This creates a **closed world investigation boundary**.

The AI can interpret the supplied evidence, but cannot independently retrieve unrelated facts from the wider system.

---

# AI Validation

AI output is treated as untrusted until validated.

The validation layer is designed to check issues such as:

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
Investigation Result
      │
      ▼
Deterministic Validator
      │
   ┌──┴──┐
   ▼     ▼
 Valid  Invalid
   │      │
   ▼      ▼
Use AI   Preserve
result   deterministic path
```

RiskSignal is designed to fail closed.

A validation failure should not change the signal or silently replace deterministic intelligence.

---

# Recommendation and Human Decision

Recommendations remain separate from the AI investigation.

The AI investigator may provide possible explanations or suggested next steps.

The canonical recommendation remains deterministic.

The final flow is:

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

RiskSignal provides structured intelligence.

The human decides what to do with it.

---

# Domain Neutral Design

RiskSignal separates the **platform intelligence model** from domain specific data.

The architecture is:

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

Data Governance is currently the first domain adapter.

The same architecture could eventually support:

* Technology Risk
* Cybersecurity Risk
* AI Risk
* Operational Risk
* Financial Risk
* Market Intelligence
* Business Operations
* Supply Chain Risk

The domain adapter translates domain specific data into the canonical model.

The downstream intelligence architecture remains substantially the same:

**Context → Detection → Patterns → Signals → Evidence → Significance → Investigation → Recommendation → Decision**

The expansion is a hypothesis to be tested, not a claim that every domain will behave the same way.

---

# Testing Philosophy

Testing is a central part of the project.

The goal is not only to test whether a signal appears.

It is also to test whether a signal **does not** appear when the required conditions are absent.

Controlled scenarios provide known expected outcomes.

This makes it possible to test:

* Expected signals
* Expected non signals
* Temporal boundaries
* Evidence completeness
* Pattern composition
* Relationship validity
* AI evidence boundaries
* Validation behaviour

One of the lessons from implementation is that testing exposes assumptions that are easy to miss when a system exists only as an architecture diagram.

---

# Technology Stack

The current project uses a lightweight local stack:

* Python
* SQL
* DuckDB
* Synthetic enterprise data
* Pytest

The project intentionally avoids unnecessary infrastructure while the intelligence model is being validated.

There is currently no requirement for:

* Cloud infrastructure
* Kubernetes
* Microservices
* Production APIs
* Vector databases
* Agent frameworks

The priority is to validate the intelligence, evidence model and evaluation approach before adding infrastructure for its own sake.

---

# What Comes Next

The next stages are focused on increasing the complexity and usefulness of the intelligence layer.

### 1. More complex scenarios

Create scenarios involving more entities, relationships, events and interacting signals.

### 2. Deliberately break the logic

Test where the current patterns produce false positives, false negatives or ambiguous results.

### 3. Expand relationships

Explore relationships across Data Governance, Technology and eventually Cyber.

### 4. AI assisted investigation

Introduce an investigator that operates within the closed world evidence boundary.

The AI layer will be used to:

* Investigate evidence
* Connect relevant information
* Formulate hypotheses
* Summarise findings
* Identify unknowns

It will not decide whether something is a risk.

### 5. Evaluation

Build repeatable scenarios to evaluate:

* Grounded findings
* Unsupported claims
* Evidence references
* Temporal leakage
* Contradictory evidence
* Confidence behaviour
* Recommendation alignment

The goal is to understand whether AI improves investigation quality without weakening determinism or explainability.

---

# Longer Term Hypothesis

The longer term question behind RiskSignal is:

> **Can risk monitoring move from simply reporting what has already happened toward identifying combinations of weak signals that deserve attention earlier?**

I do not yet know whether the approach will hold up with the complexity and volume of a real enterprise environment.

That is what the implementation is intended to test.

The longer term hypothesis is that the same architecture could extend beyond Data Governance and Data Quality into Technology, Cyber, AI and Operational Risk.

But that expansion needs to be earned through the implementation.

---

# Development Philosophy

RiskSignal follows a few principles:

### Determinism before AI

The system should establish what happened before asking AI to interpret it.

### Evidence before narrative

Investigations should be grounded in explicit evidence.

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
│       ├── domains/
│       │   └── data_governance/
│       ├── intelligence/
│       │   ├── ai/
│       │   ├── context.py
│       │   ├── evidence.py
│       │   ├── investigation.py
│       │   ├── pattern.py
│       │   ├── recommendation.py
│       │   ├── signal.py
│       │   └── stages.py
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

The exact repository structure will continue to evolve as the implementation develops.

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

The test suite is currently the primary executable verification of the intelligence pipeline.

---

# Project Status

**IN DEVELOPMENT · GROUND TRUTH VALIDATION**

RiskSignal is intentionally evolving.

The current focus is validating the deterministic intelligence foundation using controlled synthetic scenarios.

The project is:

* Early
* Synthetic
* Incomplete
* Local
* Tested

It is not a production risk platform.

The goal is to build, test, break, learn and refine the underlying approach before expanding the system.

**Build → Test → Break → Learn → Refine → Expand**

---

# Disclaimer

RiskSignal is an independent personal project using synthetic data.

It does not use employer confidential information, production data, proprietary datasets or confidential business logic.

The project is intended to explore concepts in:

* Data Governance
* Risk Intelligence
* Data and Analytics
* AI assisted investigation
* Explainable intelligence
* Temporal reasoning
* Evidence based decision support
* Domain neutral architecture
