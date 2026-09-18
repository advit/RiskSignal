# RiskSignal

## AI Powered Risk Intelligence

**RiskSignal** is a synthetic enterprise risk intelligence platform designed to detect noteworthy changes, identify meaningful patterns, surface signals, preserve the evidence supporting them, and provide explainable investigation and recommendations.

The platform is designed to be **domain neutral**.

Data Governance is the first implemented domain adapter. The same underlying architecture can eventually be extended to areas such as Technology Risk, Cybersecurity Risk, AI Risk, Operational Risk, and other domains where meaningful situations emerge from relationships between entities, observations, events, patterns, and context.

> **The goal is not simply to identify a bad metric or a broken control. The goal is to understand when changing conditions form a meaningful pattern, why that pattern may matter, and what evidence supports further attention or investigation.**

---

# Why RiskSignal?

Traditional monitoring systems often focus on individual measurements:

* Is the data complete?
* Is it accurate?
* Did it arrive on time?
* Did a threshold breach?
* Is an owner assigned?
* Is a control operating?

These measurements are useful, but individual measurements rarely tell the complete story.

Meaningful situations often emerge from **relationships between multiple conditions over time**.

For example:

```text
Quality deterioration
        +
Loss of accountability
        +
Critical business exposure
        ↓
Meaningful risk signal
```

RiskSignal therefore separates the problem into several stages:

```text
Understand context
        ↓
Detect noteworthy changes
        ↓
Identify patterns
        ↓
Generate signals
        ↓
Collect evidence
        ↓
Determine significance
        ↓
Investigate
        ↓
Recommend
        ↓
Human decision
```

The deterministic layers establish what happened, what patterns are present, and what evidence supports them.

The AI layer is then given a **closed package of evidence** and asked to investigate that signal without independently inventing new evidence or changing the underlying assessment.

A useful way to think about the architecture is:

> **Triggers are what RiskSignal notices. Patterns are what RiskSignal understands. Signals are what RiskSignal surfaces. Significance describes how much attention the signal warrants.**

---

# Core Architecture

RiskSignal is built around a domain neutral canonical model and a deterministic intelligence pipeline.

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
              ┌──────────┴──────────┐
              ▼                     ▼
      Trigger Detection      Pattern Detection
              │                     │
              └──────────┬──────────┘
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
                 ┌───────┴───────┐
                 │               │
                 ▼               ▼
        Deterministic       AI Investigation
        Investigation              │
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

The architecture deliberately separates **detection**, **evidence**, **significance**, **AI investigation**, and **recommendation**.

AI does not determine whether a signal exists.

AI does not create the underlying evidence.

AI does not replace the deterministic recommendation.

AI investigates an already identified signal using evidence that has already been collected.

---

# Trigger, Pattern, and Signal

These concepts are deliberately separated.

## Trigger

A **trigger** is a noteworthy deviation from expected behavior that causes the detection engine to evaluate whether something meaningful may be developing.

A trigger could be:

* An unexpected metric change
* An anomaly
* A missed expected event
* An expired relationship
* A control condition that is no longer satisfied
* A deviation from an expected process
* A change in an expected state

A trigger does not necessarily become a pattern or a signal.

For example:

```text
Timeliness
    98%
     ↓
    91%
     ↓
Trigger
"Unexpected deterioration"
```

The deviation may be worth recording without being significant enough to form a broader pattern.

**Trigger is an intelligence concept, not a canonical object.**

---

## Pattern

A **pattern** is a deterministic interpretation of one or more observations, triggers, relationships, or events that identifies a meaningful relationship, trend, or condition.

For example:

```text
98%
 ↓
94%
 ↓
89%
 ↓
Pattern
"Consecutive metric decline"
```

A pattern represents what the deterministic engine has identified in the available data.

---

## Signal

A **signal** is a formal RiskSignal output generated from a detected pattern.

For example:

```text
Consecutive metric decline
            ↓
       Signal Generation
            ↓
Emerging deterioration signal
```

A signal represents something that RiskSignal has determined is meaningful enough to surface.

The term **signal** does not imply that every signal represents a confirmed risk. A signal is an indication that something meaningful may be developing and may warrant further attention or investigation.

This separation means that:

```text
Trigger
    ↓
Something deviated

Pattern
    ↓
Something meaningful is developing

Signal
    ↓
RiskSignal formally surfaced it
```

Not every trigger becomes a pattern, and not every pattern necessarily needs to become a signal.

---

# Significance and Attention

RiskSignal does not rely on a single universal risk score to determine whether every possible combination of conditions is significant.

Instead, detected signals can be assessed through four levels representing the degree of attention warranted by the available evidence:

### DETECTED

RiskSignal has detected a trigger or noteworthy change.

The situation is surfaced because it may be meaningful, but there is not yet enough evidence to suggest a broader developing situation.

### EMERGING

A pattern is emerging.

Signals may be persisting, strengthening, or becoming connected to other indicators.

**Emerging describes the development of a pattern. It does not mean "emerging risk" as a formal risk classification.**

### INVESTIGATE

The evidence is sufficiently meaningful that the situation should be prioritized for investigation.

RiskSignal should explain what is driving the prioritization and provide the supporting evidence.

### ATTENTION

The evidence indicates that leadership attention is warranted now.

This does not mean that earlier stages are hidden from leadership or require no response. Monitoring, review, communication, and other appropriate actions can occur at any stage.

The four levels therefore represent a progression:

```text
Something was detected
        ↓
Something is developing
        ↓
This deserves focused investigation
        ↓
Leadership attention is warranted
```

The appropriate response remains separate from the significance tier.

Significance is an assessment of **attention**, not a universal risk severity score.

---

# Domain Neutral Design

RiskSignal is not designed around Data Governance tables.

Instead, domain specific data is projected into a common canonical model.

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

These objects provide a common language for different risk domains.

**Trigger is intentionally not included as a canonical object.** It is part of the detection logic that operates on canonical observations, events, relationships, and context.

For example:

```text
Data Governance
      │
      ├── Data Asset
      ├── Owner
      ├── DQ Measurement
      └── Governance Event
             │
             ▼
       Canonical Model
```

A future Technology Risk adapter could instead project:

```text
Technology Risk
      │
      ├── Application
      ├── Technology Owner
      ├── Control Assessment
      └── Technology Event
             │
             ▼
       Canonical Model
```

The intelligence engines can then operate on the canonical representation rather than being rewritten for every domain.

---

# The Canonical Model

## Entity

A thing that can be assessed or related to other things.

Examples:

* Data asset
* Application
* Business unit
* Employee
* Technology service

---

## Relationship

A time aware relationship between entities.

Examples:

* Owner of
* Supports
* Depends on
* Reports to
* Governed by

Relationships can have effective dates.

This allows RiskSignal to determine whether a relationship was active at a particular point in time.

---

## Observation

A measured value associated with an entity at a particular time.

Examples:

* Timeliness
* Completeness
* Accuracy
* DQ score
* Control effectiveness
* Incident frequency

Observations contain separate timestamps for when something was observed and when the information became available to the system.

---

## Event

A discrete event associated with an entity or relationship.

Examples:

* Migration
* Incident
* Audit finding
* Ownership change
* Control change
* Remediation activity

Events provide context around observations and patterns.

---

## Pattern

A deterministic interpretation of one or more observations, triggers, relationships, or events that identifies a meaningful relationship, trend, or condition.

Examples:

* Consecutive metric decline
* Missing required relationship
* Compound pattern

Patterns describe **what the deterministic engine has identified**.

---

## Signal

A formal RiskSignal output generated from a detected pattern.

Examples:

* Emerging deterioration
* Missing relationship
* Compound risk

Signals reference the pattern that caused them and contain deterministic attributes describing their type, significance, and relevant context.

The term **signal** does not imply that every signal represents a confirmed risk. A signal is an indication that something meaningful may be developing and may warrant further attention.

---

## Evidence

Evidence explains why a pattern or signal exists.

RiskSignal distinguishes between:

### Constitutive evidence

Evidence that directly supports the existence of the detected pattern.

Examples:

* Declining observations
* Expired ownership relationship
* Missing required relationship

### Contextual evidence

Evidence that may help explain or investigate the signal but does not independently establish that the signal exists.

Examples:

* Migration event
* Lifecycle change
* Related contextual relationship

This distinction prevents contextual information from accidentally becoming proof.

---

## Investigation

An investigation explains the signal using the available evidence.

The investigation layer can contain:

* Findings
* Supporting evidence
* Possible explanations
* Unknowns
* Next steps
* Confidence

The investigation can be generated deterministically or, when enabled, through the AI investigation layer.

---

## Recommendation

A recommendation is generated deterministically from the signal and evidence.

AI may provide suggested next steps as part of its investigation, but the canonical recommendation remains controlled by the deterministic recommendation engine.

---

## Decision

The final human decision is deliberately separate from the automated analysis.

RiskSignal does not attempt to make the human decision automatically.

---

# Temporal Integrity

Time is a first class concept in RiskSignal.

A major architectural principle is:

> **The system must never use information that was not available at the time being evaluated.**

RiskSignal therefore distinguishes between timestamps such as:

```text
observed_at
occurred_at
available_at
detected_at
```

For example:

```text
Observation occurred
        │
        ▼
observed_at

Information became available
        │
        ▼
available_at
```

When RiskSignal evaluates an entity at a particular `as_of` timestamp, only information satisfying:

```text
available_at <= as_of
```

is eligible.

This prevents future information from leaking into historical signals or investigations.

The same principle applies to time bounded relationships.

An owner relationship that expired before `as_of` must not be treated as an active owner.

---

# Initial Data Governance Adapter

The first implemented domain is Data Governance.

The current synthetic dataset models a small fictional enterprise environment containing:

* Business units
* Employees
* Data assets
* Data asset ownership
* Data quality rules
* Data quality measurements
* Governance events

The primary demonstration asset is:

**DA047 — Credit Exposure Amount**

The dataset is intentionally synthetic.

It is designed to create realistic conditions that allow RiskSignal to demonstrate:

* Data quality deterioration
* Ownership changes
* Missing or expired relationships
* Compound risk
* Migration context
* Temporal reasoning
* Evidence construction

---

# Data Quality

The initial Data Governance adapter calculates a composite Data Quality Score from four dimensions:

### Completeness

Whether required values are present.

### Accuracy

Whether observed values agree with an authoritative source or approved reconciliation rule.

### Timeliness

Whether data is available within the expected service level.

### Uniqueness

Whether records satisfy the relevant uniqueness expectation.

The current composite score is:

```text
DQ Score =
    0.30 × Completeness
  + 0.30 × Accuracy
  + 0.20 × Timeliness
  + 0.20 × Uniqueness
```

Where:

```text
Uniqueness = 100 − Duplicate Rate
```

The underlying measurements remain available rather than treating the composite score as the only source of truth.

---

# Deterministic Intelligence

The current MVP focuses on deterministic intelligence before introducing a live LLM.

The pipeline is deliberately explicit:

```text
Context
   ↓
Trigger Detection
   ↓
Pattern Detection
   ↓
Signal Generation
   ↓
Evidence
   ↓
Significance
   ↓
Investigation
   ↓
Recommendation
```

Trigger detection and pattern detection are both part of the **Detection Engine**.

A trigger does not automatically become a pattern, and a pattern does not automatically become a signal.

---

## Context

The Context Engine assembles the time valid information relevant to an entity.

This includes:

* Observations
* Relationships
* Events
* Entity attributes

---

## Triggers

Trigger detection identifies noteworthy deviations from expected behavior.

Examples include:

* Unexpected metric deterioration
* A relationship becoming inactive
* An expected event not occurring
* A control condition changing
* An observation deviating from an expected trend

A trigger can remain an isolated observation.

The detection engine determines whether one or more triggers, observations, relationships, or events form a meaningful pattern.

---

## Patterns

Pattern detection is domain neutral.

The current MVP includes:

### Consecutive Metric Decline

Identifies sustained deterioration in a metric over time.

This is intentionally generic.

The engine does not need to know whether the metric represents:

* Data quality
* Cyber incidents
* Control effectiveness
* Technology stability
* Operational performance

### Missing Relationship

Identifies when a required relationship is missing or no longer active.

For example:

```text
Data Asset
    │
    └── Owner
           │
           └── Relationship expired
```

### Compound Pattern

Combines independent pattern families.

For example:

```text
Metric deterioration
        +
Accountability gap
        ↓
Compound pattern
        ↓
Compound risk signal
```

Two measurements that represent the same underlying indicator family are not automatically treated as independent risks.

The current MVP uses deterministic rules to identify meaningful combinations.

Future versions may evaluate historical combinations to determine which combinations provide incremental intelligence and should be promoted to validated composite patterns.

The objective is not to manually score every possible combination. It is to identify combinations that demonstrably add information.

---

# Signals

Signals are generated from deterministic patterns.

Current examples include:

```text
Emerging deterioration
Missing relationship
Compound risk
```

Signals describe what RiskSignal has detected.

Their significance is assessed separately using deterministic logic and contextual attributes.

The AI layer does not decide whether these signals exist.

---

# Evidence

Every signal should be explainable from evidence.

For example:

```text
Signal
  │
  ├── Pattern
  │
  ├── Constitutive Evidence
  │      ├── Observation
  │      ├── Observation
  │      └── Relationship
  │
  └── Contextual Evidence
         └── Migration Event
```

This creates an auditable chain:

```text
Evidence
   ↓
Pattern
   ↓
Signal
```

A contextual event may help explain a signal without being treated as proof that the signal exists.

---

# AI Investigation

AI is introduced only after deterministic evidence has been constructed.

The current architecture is:

```text
Deterministic Signal
        ↓
Deterministic Evidence
        ↓
Closed Evidence Package
        ↓
AI Investigator
        ↓
Validation
        ↓
Investigation
```

The AI receives a **closed world evidence package**.

It does not have unrestricted access to the underlying dataset.

The package contains the evidence that RiskSignal has already determined is relevant.

This creates an important boundary:

> **The deterministic system determines what is known. AI interprets that known evidence.**

The AI investigator may produce:

* Summary
* Findings
* Evidence citations
* Possible explanations
* Unknowns
* Suggested next steps
* Confidence

Every finding must reference evidence from the package.

AI cannot cite an evidence ID that does not exist in the package.

AI also cannot use a contextual event as proof of a pattern that is not supported by constitutive evidence.

---

# AI Validation

AI output is treated as untrusted until validated.

The validator checks that the investigation:

* Contains the required fields
* Uses valid evidence IDs
* Does not reference evidence outside the package
* Provides evidence for findings
* Uses valid confidence values
* Does not produce malformed output

Conceptually:

```text
AI Output
    │
    ▼
Validation
    │
 ┌──┴──┐
 │     │
Valid Invalid
 │     │
 ▼     ▼
Use   Reject
 │     │
 │     └── Preserve deterministic result
 ▼
Investigation
```

This is intended to provide a controlled boundary between probabilistic AI output and deterministic risk intelligence.

---

# Recommendation

Recommendations remain deterministic.

The current recommendation layer uses the signal and evidence to produce an action oriented recommendation.

For example:

```text
Emerging deterioration
        ↓
Increase monitoring

Migration context
        ↓
Validate migration controls

Ownership gap
        ↓
Restore active accountability
```

AI may suggest additional next steps, but it does not replace the deterministic recommendation.

This separation allows the project to explore AI without making the AI model the source of truth for risk decisions.

---

# Human Decision

RiskSignal deliberately ends with a human decision.

```text
Evidence
   ↓
Signal
   ↓
Investigation
   ↓
Recommendation
   ↓
Human Decision
```

The system is intended to support decision making rather than autonomously make consequential risk decisions.

---

# Current Vertical Slice

The current implementation demonstrates an end to end Data Governance scenario around:

**DA047 — Credit Exposure Amount**

The current vertical slice includes:

```text
Synthetic Data
      ↓
Data Governance Adapter
      ↓
Canonical Projection
      ↓
Temporal Context
      ↓
Detection Engine
      ↓
Triggers
      ↓
Patterns
      ↓
Signals
      ↓
Evidence Construction
      ↓
Evidence Package
```

The deterministic investigation and recommendation layers are also implemented.

The AI boundary has now been established, but a live LLM is not yet connected.

The significance model has been defined conceptually and will be implemented as a distinct deterministic assessment layer.

---

# What Is Implemented Today

### Platform Foundation

* Domain neutral canonical model
* Entity
* Relationship
* Observation
* Event
* Pattern
* Signal
* Evidence
* Investigation
* Recommendation
* Decision

### Data Governance

* Synthetic enterprise dataset
* Data Governance adapter
* DA047 vertical slice
* Data quality measurements
* Ownership relationships
* Governance events
* DuckDB persistence

### Deterministic Intelligence

* Temporal context construction
* Temporal relationship evaluation
* Consecutive metric decline detection
* Missing relationship detection
* Compound pattern detection
* Signal generation
* Constitutive and contextual evidence
* Deterministic investigation construction
* Deterministic recommendation construction
* Human decision recording

### AI Foundation

* Evidence package contract
* Closed world evidence package
* Evidence package builder
* AI investigator interface
* Investigation result contract
* Investigation validation interface
* AI package tests

The current test suite contains **18 passing tests**.

---

# What Comes Next

The implementation will progress incrementally.

## Next: AI Investigation

Implement a non networked investigator first.

The initial investigator will behave like an AI investigator without requiring an external model.

This allows the project to test:

* Investigation structure
* Evidence citations
* Validation
* Failure handling
* Grounding rules

before introducing an actual LLM.

---

## Then: AI Validation

Build validation rules for cases such as:

```text
Unknown evidence ID
        ↓
Reject

Finding without evidence
        ↓
Reject

Malformed confidence
        ↓
Reject

Valid evidence grounded investigation
        ↓
Accept
```

---

## Then: Local LLM

Connect a local model through an explicit Investigator implementation.

The deterministic architecture remains unchanged.

Conceptually:

```text
Evidence Package
       ↓
Local LLM
       ↓
Structured InvestigationResult
       ↓
Validator
       ↓
Accepted Investigation
```

The model becomes replaceable because the rest of RiskSignal depends only on the Investigator contract.

---

## Later: Tool Calling

Once the basic LLM investigation works reliably, the investigator can eventually be extended to use controlled tools.

For example:

```text
AI Investigator
      │
      ├── inspect evidence
      ├── examine related entity
      ├── inspect temporal history
      └── compare observations
```

Tool access would remain controlled and auditable.

---

## Later: Evaluation

The project will eventually include structured evaluation of AI investigations.

Potential evaluation dimensions include:

* Evidence grounding
* Unsupported claims
* Citation accuracy
* Completeness
* Consistency
* Temporal correctness
* Recommendation alignment

The goal is to evaluate whether AI is producing useful investigations rather than simply producing fluent text.

---

# Future Domain Expansion

Once the domain neutral intelligence pipeline is established, additional adapters can be introduced.

Potential future domains include:

```text
Data Governance
      │
      ├── Technology Risk
      ├── Cybersecurity Risk
      ├── AI Risk
      ├── Operational Risk
      └── Other risk domains
```

The objective is not to create a separate RiskSignal application for every risk domain.

The objective is to allow different domains to project their data into the same intelligence architecture.

---

# Future Risk Intelligence Use Cases

The architecture is intentionally broader than the initial Data Governance use case.

The same principles could eventually be applied to problems such as:

* Technology control deterioration
* Cybersecurity risk patterns
* AI governance risk
* Operational control deterioration
* Vendor risk
* Application lifecycle risk
* Financial or market signal monitoring
* Other domains where multiple observations and events need to be connected over time

These are future applications of the architecture, not capabilities currently claimed by the MVP.

---

# Technology Stack

The initial development stack is intentionally lightweight.

* **Python** — core implementation
* **SQL** — analytical querying
* **DuckDB** — local analytical persistence
* **pandas** — data manipulation
* **NumPy** — numerical computation
* **pytest** — automated testing
* **Jupyter** — experimentation and learning
* **Matplotlib** — visualization
* **Git / GitHub** — version control

AI model infrastructure will be introduced only when the deterministic and evidence boundaries are sufficiently mature.

The project deliberately avoids unnecessary infrastructure such as:

* Cloud services
* Microservices
* Kubernetes
* Postgres
* Vector databases
* RAG frameworks
* Agent frameworks

until the project demonstrates a concrete need for them.

---

# Development Philosophy

RiskSignal is both a **working prototype** and a **technical learning project**.

The development approach emphasizes:

1. Understanding the risk problem before implementing AI
2. Building deterministic logic before probabilistic logic
3. Generating underlying synthetic data rather than arbitrary scores
4. Preserving temporal integrity
5. Separating trigger detection from pattern recognition
6. Separating detection from investigation
7. Preserving evidence for explainability
8. Treating AI output as untrusted until validated
9. Keeping significance assessment explicit and explainable
10. Keeping recommendations deterministic
11. Keeping humans in the decision loop
12. Starting with a small vertical slice before expanding the architecture

The project intentionally spends more effort on **intelligence, reasoning, evidence, evaluation, and learning** than on infrastructure.

---

# Repository Structure

```text
src/risksignal/
│
├── canonical/
│   └── models.py
│
├── intelligence/
│   ├── ai/
│   │   ├── contracts.py
│   │   ├── package.py
│   │   └── ...
│   │
│   ├── context.py
│   ├── evidence.py
│   ├── investigation.py
│   ├── pattern.py
│   ├── recommendation.py
│   ├── signal.py
│   └── stages.py
│
├── adapters/
│   └── data_governance/
│
├── persistence/
│
└── pipeline.py

tests/
├── unit/
└── integration/
```

The repository is intentionally structured around **canonical objects and reusable intelligence stages**, rather than around a single domain.

---

# Running the Project

Run the following from the repository root with the project virtual environment activated:

```text
pip install -e ".[dev]"
pytest
```

The current test suite validates the deterministic intelligence pipeline and the initial AI evidence package boundary.

---

# Project Status

**Current stage: Domain neutral Risk Intelligence MVP with Data Governance as the first domain adapter**

The deterministic intelligence pipeline is implemented.

The AI boundary is implemented.

The significance model has been defined conceptually and will be implemented as a separate deterministic assessment layer.

The next milestone is the **AI investigation and validation layer**, followed by connection to a local LLM.

The current architecture is intentionally designed so that introducing an LLM does not require redesigning the deterministic risk intelligence pipeline.

---

# Disclaimer

RiskSignal uses synthetic data and a conceptual enterprise architecture.

It is an experimental prototype intended to demonstrate concepts in:

* Data
* Analytics
* Risk intelligence
* Data governance
* Machine learning
* AI investigation
* Evidence based reasoning

It is not a production banking risk management system and does not represent the systems, controls, methodologies, or practices of any specific financial institution.
