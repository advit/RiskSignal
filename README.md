# RiskSignal

## AI-Powered Data Risk Intelligence

**RiskSignal** is a synthetic-but-realistic enterprise data risk intelligence platform designed to detect emerging data risk before it becomes a material business, regulatory, or operational issue.

The platform combines **data quality, semantic consistency, governance, maturity, business exposure, lifecycle, and audit context** to identify emerging risk, predict potential deterioration, investigate contributing factors, and recommend action.

> **The goal is not simply to identify bad data. The goal is to understand when data becomes a business risk.**

---

## Why RiskSignal?

Traditional data quality monitoring often focuses on questions such as:

* Is the data complete?
* Is it accurate?
* Did the data arrive on time?
* Are there duplicates?
* Did a quality score breach a threshold?

These are necessary, but they do not tell the complete risk story.

The same data quality result can have very different implications depending on:

* How critical the data is
* Whether it supports Board or regulatory reporting
* How mature the underlying metric and controls are
* Whether the metric is highly automated or heavily dependent on manual intervention
* Whether an authoritative source exists
* Whether different teams use different definitions or calculation methods
* Whether second-line governance has confidence in the metric
* Whether there are open audit findings
* Whether remediation is progressing
* Whether the metric is being migrated, redesigned, or otherwise changing

RiskSignal brings these signals together.

---

## Core Concept

RiskSignal is built around the idea that **data quality is one component of data risk, not the definition of data risk.**

```text
                         CDE / Metric
                              │
          ┌───────────────────┼────────────────────┐
          │                   │                    │
          ▼                   ▼                    ▼
   Data Quality       Semantic / Consistency   Governance
          │                   │                    │
          │                   │              ┌─────┴─────┐
          │                   │              │           │
          │                   │          Maturity    Validation
          │                   │
          └───────────────────┼────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
       Business Exposure              Lifecycle / Risk Context
              │                               │
              │                       Audit / Remediation
              │                       Migration / Evolution
              │                       Incidents
              │
              └───────────────┬───────────────┘
                              ▼
                       Risk Assessment
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
          ML Risk Prediction        AI Investigation
                 │                         │
                 └────────────┬────────────┘
                              ▼
                       Recommendation
                              │
                              ▼
                       Human Decision
```

---

## Initial Use Case

The first machine learning problem is intentionally narrow:

> **Predict whether a critical data asset's Data Quality Score will breach its expected threshold within the next 30 days.**

The initial experiment uses:

* A 90-day observation window
* A 30-day prediction window
* Critical Data Element: **DA047 — Credit Exposure Amount**
* Composite DQ breach threshold: **80**

The initial ML problem is deliberately constrained so that the end-to-end approach can be validated before expanding the model.

---

## Data Quality

RiskSignal initially measures four dimensions:

### Completeness

Whether required values are present.

### Accuracy

Whether the observed value agrees with an authoritative source or approved reconciliation rule.

### Timeliness

Whether data is available within the required service-level expectation.

### Duplicate Rate

The proportion of records that violate the relevant uniqueness expectation.

The initial composite score is:

```text
DQScore =
    0.30 × Completeness
  + 0.30 × Accuracy
  + 0.20 × Timeliness
  + 0.20 × (100 − DuplicateRate)
```

The underlying measurements are retained rather than treating the composite score as the only source of truth.

---

## Accuracy and Authoritative Sources

RiskSignal does not assume that accuracy means simply checking whether a value falls within a valid range.

For example, a credit score between 0 and 850 may be valid while still being incorrect.

Accuracy may instead require comparison against an **authoritative source**.

For example:

```text
Authoritative Source
        │
        ▼
Exposure_Master
        │
        ├──────────────► Risk Reporting
        │
        ├──────────────► Regulatory Reporting
        │
        └──────────────► Executive Reporting
```

Downstream representations can then be evaluated using approved reconciliation rules, tolerances, effective dates, populations, and calculation logic.

---

## Semantic Consistency

Data risk is not always caused by bad underlying data.

Different teams may produce different values because they use:

* Different source systems
* Different business definitions
* Different calculation formulas
* Different populations
* Different effective dates
* Different rounding or precision rules
* Different transformation logic

RiskSignal therefore treats **semantic and calculation consistency** as a distinct source of risk.

A difference between two values is not automatically classified as an error. The system should investigate *why* the values differ.

---

## Maturity

Maturity is treated as a **composite assessment**, not simply the age of a metric.

Potential maturity factors include:

* Age and operating history
* Level of automation
* Manual intervention
* Validator and regulator confidence
* Fit for purpose
* Documentation quality
* Control strength
* Lineage and traceability

This allows RiskSignal to distinguish between situations such as:

```text
New metric
+ highly automated
+ fully documented
+ independently validated
+ fit for purpose
        ↓
Potentially high maturity
```

and:

```text
Long-established metric
+ manual processing
+ significant interdependence
+ weak documentation
+ limited validation
        ↓
Potentially low maturity
```

The component evidence is retained so that maturity assessments can be explained rather than treated as an opaque number.

---

## Business Exposure

The significance of a data issue depends on what the data supports.

RiskSignal therefore considers exposure such as:

* Board and executive reporting
* Regulatory reporting
* Enterprise KPIs and KRIs
* Material business decisions
* Functional reporting
* Local or exploratory analysis

A DQ score of 78 does not necessarily represent the same risk for every metric.

---

## Governance and Second-Line Validation

RiskSignal distinguishes operational data quality from independent governance assessment.

For example:

```text
First Line
    │
    └── DQ Score = 87.5

Second Line
    │
    └── Governance Assessment = Needs Improvement
```

The data may currently be within the DQ threshold while governance weaknesses indicate emerging risk.

This distinction is important for understanding risk that may not yet appear in operational quality measurements.

---

## Lifecycle and Known Issues

Metrics and data assets evolve.

RiskSignal captures contextual states such as:

* New metric
* Established metric
* Metric being enhanced
* Migration
* Deprecation
* Open audit finding
* Remediation in progress
* Validation pending
* Incident history

A known issue is **not automatically treated as no risk**.

RiskSignal should be able to determine whether:

* Remediation is progressing
* Risk is increasing or decreasing
* Deadlines are being missed
* Impact is expanding
* New risk is emerging outside the known issue

---

## Machine Learning

The initial ML model focuses on predicting future DQ deterioration.

The project deliberately separates:

### Predictive features

Information available at the time of prediction that may help forecast future risk.

### Context

Information that helps determine the significance of a predicted event.

### Investigation evidence

Information used after a signal is generated to understand the underlying cause.

This separation helps prevent temporal leakage and avoids creating a model that simply throws every available field into a prediction algorithm.

A core principle is the **"9:00 AM test"**:

> If the model could not have known the information at 9:00 AM on the prediction date, it cannot be used as a predictive feature for that prediction.

---

## AI Investigation

Machine learning answers questions such as:

> **What is likely to happen?**

The AI investigation layer is intended to answer:

> **Why is this happening?**

and:

> **What should we do about it?**

The investigation layer may eventually examine:

* DQ trends
* Quality rule failures
* Authoritative-source reconciliation
* Metric definitions
* Calculation formulas
* Lineage
* Ownership
* Governance assessments
* Validator feedback
* Audit findings
* Remediation status
* Lifecycle changes

The objective is not simply to retrieve documents. It is to **reason across multiple sources of evidence** and produce an explainable risk narrative.

---

## Example Risk Narrative

An eventual RiskSignal output might look conceptually like:

```text
Risk Signal

DA047 — Credit Exposure Amount

Predicted Risk:
High likelihood of DQ breach within 30 days.

Evidence:
• Timeliness has deteriorated for 14 consecutive days.
• Duplicate rate has increased steadily.
• Downstream Risk Reporting is dependent on DA047.
• The metric supports an enterprise risk indicator.
• An open remediation item exists for the upstream ingestion process.
• Second-line confidence has declined.
• The metric is currently undergoing a platform migration.

Assessment:
The emerging risk appears to be driven primarily by
upstream processing instability during migration rather
than a deterioration in the metric definition itself.

Recommendation:
Increase monitoring frequency, validate the migration
control, and prioritize remediation of the upstream
processing issue.
```

This is the eventual direction of the platform, not a claim that all of these capabilities are already implemented.

---

## Architecture Approach

RiskSignal is being developed incrementally.

The project has an enterprise-scale conceptual architecture, but implementation begins with a deliberately small vertical slice.

### Phase 1 — Vertical Slice

Focus on one Critical Data Element:

**DA047 — Credit Exposure Amount**

The objective is to demonstrate the complete journey:

```text
Underlying Data
      ↓
Quality Rules
      ↓
DQ Measurements
      ↓
DQ Score
      ↓
Risk Context
      ↓
Risk Signal
      ↓
ML Prediction
      ↓
AI Investigation
      ↓
Recommendation
```

The implementation will expand only after the vertical slice is understood and validated.

---

## Technology Stack

The initial development stack is intentionally lightweight:

* **Python** — data processing, feature engineering and ML
* **SQL** — analytical querying
* **DuckDB** — local analytical database
* **pandas** — data manipulation
* **NumPy** — numerical computation
* **scikit-learn** — machine learning
* **Jupyter** — experimentation and learning
* **Matplotlib / Seaborn** — analysis and visualization
* **Git / GitHub** — version control

Additional technologies will be introduced only when they solve a demonstrated problem.

---

## Development Philosophy

RiskSignal is being built as both a **working prototype** and a **technical learning project**.

The development approach emphasizes:

1. Understanding the business problem before implementing the model
2. Generating underlying data rather than arbitrary scores
3. Building rules before building ML
4. Understanding SQL and Python through hands-on implementation
5. Separating predictive modeling from post-signal investigation
6. Maintaining temporal integrity and preventing data leakage
7. Preserving evidence for explainability
8. Starting small and expanding incrementally

---

## Project Status

**Current stage: Domain-neutral core + Data Governance adapter MVP**

The runtime is a locally runnable Python package. Data Governance is the first domain adapter; it is not the platform core.

Completed:

* Canonical model: Entity, Relationship, Observation, Event, Pattern, Signal, Evidence, Investigation, Recommendation, Decision
* DuckDB persistence (`governance` and `canonical` schemas)
* Data Governance tables and synthetic DA047 seed
* Adapter projection into the canonical model
* Domain-neutral Context, Pattern, Signal, and Evidence engines
* Deterministic investigation / recommendation builders and human decision recording
* Unit and end-to-end tests for an explainable DA047 signal

Next:

* Expand pattern coverage without adding domain-specific engines
* Develop the initial ML experiment on canonical observations (temporal integrity preserved)
* Add an isolated AI investigation interface on top of Evidence / Investigation

Layout:

```text
src/risksignal/canonical/       # domain-neutral objects
src/risksignal/intelligence/    # reusable engines
src/risksignal/adapters/data_governance/
src/risksignal/persistence/     # DuckDB
tests/unit/  tests/integration/
```

Run tests from the repo root (with the project venv):

```text
pip install -e ".[dev]"
pytest
```

---

## Disclaimer

RiskSignal uses synthetic data and a conceptual enterprise architecture. It is an experimental prototype intended to demonstrate data, analytics, machine learning, AI, and data governance concepts.

It is not a production banking risk management system and does not represent the systems, controls, methodologies, or practices of any specific financial institution.
