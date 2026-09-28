# Pack Manager Architecture

The Pack Manager is an evidence-first, headless verification system. It separates request handling, image/model verification, decision logic, evidence records, storage, and downstream operational review.

---

## Contents

1. [Architecture Flow](#architecture-flow)
2. [Main Components](#main-components)
3. [End-to-End Flow](#end-to-end-flow)
4. [Safety Principle](#safety-principle)

---

## Architecture Flow

    +-----------------------------------+
    |        Verification Request       |
    +-----------------------------------+
                      |
                      v
    +-----------------------------------+
    |          Request Parser           |
    |  - Parse request                  |
    |  - Validate required data         |
    +-----------------------------------+
                      |
                      v
    +-----------------------------------+
    |        Verification Service       |
    |  - Tenant/org validation          |
    |  - Workflow orchestration         |
    +-----------------------------------+
                      |
                      v
    +-----------------------------------+
    |      Image / Model Boundary       |
    |  - Image reference                |
    |  - Vision model provider          |
    |  - Structured observation         |
    +-----------------------------------+
                      |
                      v
    +-----------------------------------+
    |        Verification Pipeline      |
    |  - Item presence                  |
    |  - Quantity                       |
    |  - Extra items                    |
    |  - Evidence sufficiency           |
    +-----------------------------------+
                      |
                      v
    +-----------------------------------+
    |           Decision Layer          |
    |  - PASS                           |
    |  - FAIL                           |
    |  - UNCERTAIN                      |
    |  - PENDING_REVIEW                 |
    +-----------------------------------+
                      |
           +----------+----------+
           |                     |
           v                     v
    +----------------+   +------------------+
    | Evidence/Record|   |  Human Override  |
    | - Evidence     |   | - Review         |
    | - Reasoning    |   |   uncertain      |
    | - Model status |   | - Auditable      |
    +----------------+   |   decision       |
           |             | - Override record|
           |             +------------------+
           v
    +-----------------------------------+
    |   Organisation-Scoped Storage     |
    +-----------------------------------+

---

## Main Components

### 1. Request Parsing and Validation

The request layer accepts the verification request and converts it into the internal request model. The request contains:

- Organisation context
- Unit information
- Expected package contents
- Image reference

Validation ensures that required information is present before the verification workflow proceeds.

**Modules:** `request_parser.py`, `validation.py`, `models.py`

---

### 2. Tenant and Organisation Context

Every verification request is associated with an organisation. The tenant layer validates the organisation context and ensures that records are stored and retrieved using the correct organisation scope.

This prevents a verification record belonging to one organisation from being treated as a record belonging to another organisation.

**Modules:** `tenant.py`, `storage.py`

---

### 3. Verification Service

The verification service coordinates the complete verification workflow. It connects request validation, model execution, verification logic, record creation, and persistence.

The service does not make unsupported assumptions when a model result is unavailable.

**Modules:** `service.py`, `pipeline.py`

---

### 4. Image and Model Boundary

The image/model boundary separates the verification system from the external vision or AI provider. The system passes the image reference and expected package contents to the model boundary and expects a structured observation.

The current implementation uses a provider-neutral `ModelClient`. If no model provider is configured, the system does not fabricate observations. Instead, it returns an explicit model configuration error and produces `PENDING_REVIEW`.

**Modules:** `image.py`, `model_client.py`, `config.py`

---

### 5. Verification Pipeline

The verification pipeline compares the expected package contents with the observed contents returned by the model boundary. It evaluates four primary checks:

1. Item presence
2. Quantity
3. Extra items
4. Evidence sufficiency

The pipeline keeps expected contents and observed contents separate so that downstream decisions remain traceable.

**Modules:** `pipeline.py`, `verifier.py`

---

### 6. Decision Layer

The decision layer converts the verification checks into an operational verdict. Supported outcomes:

- `PASS`
- `FAIL`
- `UNCERTAIN`
- `PENDING_REVIEW`

The system is intentionally conservative. When evidence is insufficient or the model cannot provide a usable result, the workflow does not claim a successful verification. Instead, it produces `UNCERTAIN` or `PENDING_REVIEW` as appropriate.

**Modules:** `verifier.py`, `pipeline.py`, `records.py`

---

### 7. Evidence and Verification Records

The system produces a structured verification record containing the request context, expected contents, observed contents, individual checks, evidence, reasoning, model status, and final verdict.

The record provides a traceable representation of how the decision was produced.

**Modules:** `records.py`

---

### 8. Human Override

Automated verification is not treated as irreversible. When an operator reviews an uncertain or incorrect automated result, an override can be recorded separately.

The override record preserves the original automated decision and records the human decision and reason.

**Modules:** `override.py`

---

### 9. Organisation-Scoped Storage

Verification records are persisted under organisation-specific storage paths. For example:

    data/
    +-- verification_records/
        +-- <organisation_id>/
            +-- <record_id>.json

Runtime records are excluded from version control.

**Modules:** `storage.py`

---

### 10. Headless Agent

The agent provides a command-line workflow for executing verification without requiring a graphical interface. It accepts structured input, runs the verification workflow, and produces structured output.

The agent is designed to be deterministic at the software-contract level and suitable for automated evaluation.

**Modules:** `runner.py`, `__main__.py`, `agent/`

---

### 11. API Boundary

The API layer provides an integration boundary for applications that need to submit verification requests or consume verification results. It keeps the external interface separate from the internal verification implementation.

**Modules:** `api.py`

---

### 12. Failure Handling

Failures at the model or API boundary are converted into explicit operational states instead of being hidden or treated as successful verification. Examples include:

- Model provider not configured
- Model/API exception
- Invalid image reference
- Insufficient evidence
- Ambiguous image evidence

The key safety rule:

    Unable to verify safely
            |
            v
      PENDING_REVIEW

The system must never invent observed contents simply to produce a `PASS` or `FAIL` result.

---

## End-to-End Flow

1. Receive verification request
2. Validate request
3. Validate organisation context
4. Send image/reference to model boundary
5. Receive structured observations
6. Check item presence
7. Check quantity
8. Check extra items
9. Check evidence sufficiency
10. Produce operational verdict
11. Create evidence/decision record
12. Persist organisation-scoped record
13. Human review/override when required

---

## Safety Principle

Evidence first, decision second.

The system must distinguish between what the model observed, what the verification logic concluded, and what a human operator may later override. When reliable automated evidence is unavailable, the correct behaviour is to request human review rather than fabricate certainty.