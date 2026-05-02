# Consequence Control Stack Artifact v0.1

Status: bounded artefact. No implementation. No adoption claim.

## 1. Control question

What prevents consequence-producing action from reaching decision-ready state or execution too early within a governed workflow?

## 2. Core invariant

Within a governed workflow, no consequence-producing action may bind unless:

1. the pause state is resolved;
2. the action has validly entered decision-ready state; and
3. valid execution authority is present at the execution boundary.

## 3. Scope

This artefact applies to designated governed workflows.

A governed workflow is a workflow explicitly routed through this state model because it can affect external obligations, user-visible behaviour, access, notifications, payments, escalations, queues, safety posture, or audit posture.

Extension beyond governed workflows is optional.

Claims in this artefact apply only to decisions represented in this stack.

Current status: design and test harness only. No canonical runtime implementation is shipped with this version.

## 4. Minimum seriousness baseline

To qualify as a governed workflow under this stack, a workflow must define and maintain a versioned policy file.

A configuration weaker than this baseline may use the language of the model, but must not claim conformance with this artefact.

The policy file must specify:

- workflow identifier and scope
- technical owner
- business owner
- risk owner
- inclusion criteria
- exclusion criteria with justification
- governed resource identifiers
- required evidence fields
- evidence validation rules
- evidence currency / maximum evidence age
- bypass detection owner
- bypass detection cadence
- bypass failure response
- receipt storage method
- tamper-evidence method
- conflict detection rule
- revocation / cancellation rule

Minimum required evidence fields for every governed workflow:

- risk classification
- affected systems and resources
- alternatives considered
- applicable policy, standard, or control reference
- expected external consequence
- rollback or refusal path

Validation must be performed by either:

1. automated checks encoded in the governed workflow; or
2. an approver distinct from the proposer.

Self-validation alone is non-conformant.

Bypass checks must run at least per release or quarterly, whichever occurs first.

Detected bypass must be recorded as a separate governed event with remediation status.

Receipts must be anchored in a tamper-evident store, such as an append-only log or chained hashes using `previous_hash`.

## 5. Layer model

```text
attempted action
    ↓
Consequence Pause Layer
    ↓
decision-ready action
    ↓
Execution Boundary
    ↓
consequence or refusal
```

## 6. Layer 1 — Consequence Pause Layer

### Purpose

Prevent a response, AI output, automation, operational proposal, or human reaction from becoming decision-ready before readiness has resolved.

### Invariant

No consequence-producing action may enter decision-ready state while pause is unresolved.

### Stop point

The system physically stops before a decision becomes operationally actionable.

### Decision-ready definition

`DECISION_READY` means all required evidentiary fields are present and validated.

If any required field is missing, invalid, unresolved, stale, or contested, the action must remain `PAUSED` or move to a refusal state.

### Operationally actionable definition

A decision is operationally actionable when it contains enough specific detail to trigger a change in code, configuration, data, access, workflow state, notification, payment, escalation, obligation, or external instruction without new design choices.

### Required evidence

- attempted action
- pause trigger condition
- hold state
- release condition
- continued-hold evidence where release is refused
- supporting evidence URI

### Refusal semantics

If the pause is unresolved, the action must not proceed to decision-ready state.

The system must return a refusal or continued-hold receipt.

## 7. Layer 2 — Execution Boundary

### Purpose

Prevent a decision from binding into consequence without valid authority.

### Invariant

No state mutation without valid authority at execution.

### Stop point

The system physically stops before consequence binds.

### Required evidence

- decision-ready action
- authority verification
- allow / refuse / escalate result
- execution trace or non-execution trace
- audit receipt
- downstream state check where applicable

### Refusal semantics

If authority is absent, expired, unscoped, revoked, replayed, or unresolved, the decision must not bind.

The system must return a refusal receipt.

## 8. State model requirements

States must be mutually exclusive for a given attempted action.

A state transition is valid only when its entry condition, permitted actions, forbidden actions, and exit condition are recorded.

| State | Entry condition | Permitted actions | Forbidden actions | Exit condition |
|---|---|---|---|---|
| PROPOSED | An actor or system creates an attempted action record. | Record intent, classify action type, evaluate pause trigger. | Send, notify, escalate, mutate state, create external obligation, mark as approved. | Pause trigger evaluated. |
| PAUSED | Pause trigger fires or readiness/authority/recovery is unresolved. | Hold, gather context, request authority, continue hold, refuse release. | Enter execution queue, notify external party, mutate state, create binding instruction. | Release condition satisfied, evidence expired, release refused, or action cancelled. |
| DECISION_READY | Required evidentiary fields are present, validated, current, and linked to the action record. | Submit for authority verification, attach evidence, request approval, revoke/cancel with reason. | Bind, execute, reuse prior authority without verification, proceed with stale evidence. | Authority allowed, refused, escalated, evidence expired, revoked, or cancelled. |
| AUTHORISED | Valid scoped authority is verified for the exact action. | Execute within scope, record authorisation, prepare audit receipt. | Execute outside scope, replay authority, alter target/action without new authority. | Execution completed, refused, expired, revoked, or cancelled. |
| BINDING | Consequence-producing transition has executed under valid authority. | Record final trace, emit audit receipt, link evidence. | Modify receipt silently, erase prior states, hide bypass path. | Final receipt emitted. |
| REVOKED_CANCELLED | A PAUSED, DECISION_READY, or AUTHORISED item is withdrawn, revoked, expired, or cancelled before binding. | Record reason, timestamp, actor, affected resources, and linked prior state. | Reuse same decision instance for execution. | Terminal for that decision instance. |

## 9. Conflict, revocation, and stale evidence

For governed workflows, decisions must reference governed resources.

The system must detect and record conflicting `DECISION_READY`, `AUTHORISED`, or `BINDING` decisions against the same governed resource.

The artefact does not require automatic conflict resolution, but conflict detection must produce a receipt or governed event.

A `DECISION_READY` or `AUTHORISED` item may transition to `REVOKED_CANCELLED` before binding.

Revocation or cancellation must include reason, timestamp, actor, affected resources, and linked prior state.

Each governed workflow must define evidence currency.

If evidence exceeds its permitted age while `PAUSED`, `DECISION_READY`, or `AUTHORISED`, the decision must re-collect or re-validate evidence before proceeding.

## 10. Mandatory coverage

A minimal deployment may start with one governed workflow and a single receipt registry.

Broader coverage is incremental, not required for this artefact.

Within a governed workflow, emergency changes, feature flags, shadow deployments, direct database writes, model-triggered workflow calls, manual overrides, and out-of-band messages must either pass through the stack or be recorded as bypass violations.

Implementers must define at least one bypass detection mechanism, such as periodic trace comparison between downstream event logs and stack receipts.

A detected bypass is a separate governed event.

## 11. Failure class

### Premature decision

A premature decision occurs when a response, output, automation, operational proposal, or human reaction reaches decision-ready state before readiness, authority, or recovery has resolved.

This is distinct from unauthorised execution.

Premature decision happens before the execution gate.

## 12. Minimum failure test

### Scenario

A user receives an emotionally charged message and drafts an immediate reply that would notify another person.

### Expected control behaviour

1. The attempted reply triggers the Consequence Pause Layer.
2. The reply is held before decision-ready state.
3. No notification is sent.
4. No external consequence occurs.
5. The system records the attempted action, pause trigger, hold state, and non-release evidence.
6. Only after pause resolution may the action reach the execution boundary.

### Passing result

The attempted reply does not become decision-ready and does not produce external consequence while pause is unresolved.

### Failing result

The reply reaches send / notify / escalate state before pause resolution.

## 13. Proof surface

A valid artefact must show:

- attempted action
- governed workflow policy reference
- pause trigger
- hold state
- resolution or continued hold
- state transition evidence
- evidence validation result
- evidence currency result
- supporting evidence URI
- authority check where applicable
- allow / refuse / escalate outcome
- conflict check result
- execution or non-execution trace
- audit receipt
- bypass check result
- downstream state check where applicable

## 14. Minimum receipt fields

```text
receipt_id:
decision_id:
attempted_action_id:
attempted_action_type:
workflow_policy_reference:
policy_version:
initiator_identity:
actor_type:
reviewer_identity:
technical_owner:
business_owner:
risk_owner:
affected_systems:
affected_resources:
governed_resource_ids:
pause_trigger:
previous_state:
current_state:
state_transition_timestamp:
required_evidence_fields:
evidence_validation_result:
evidence_currency_result:
release_condition:
release_result:
authority_state:
authority_scope:
authority_expiry:
authority_revocation_status:
conflict_check_result:
override_status:
contested_status:
revocation_or_cancellation_reason:
outcome:
external_consequence:
downstream_state_check:
bypass_check_result:
evidence_uri:
previous_hash:
record_hash:
tamper_evidence_store:
timestamp:
```

Receipts attest to process and must reference supporting evidence.

A receipt without linked evidence only proves declared process, not factual prevention.

## 15. Claim limit

This artefact does not prove that a human decision is correct.

It does not prove that all governance risk is solved.

It proves a narrower control claim within governed workflows and decisions represented in this stack:

- premature decision-ready state was prevented under the tested condition; and
- unauthorised consequence did not bind under the tested condition.

Demonstrating broader reductions in premature decision formation requires deployment evidence not included here.

## 16. Non-claim boundary

This is not a full runtime.

This is not a product claim.

This is not an endorsement, adoption, partnership, or market-validation claim.

This is a bounded control artefact for inspection.

## 17. Clean line

The pause prevents decisions from becoming actionable too early.

The gate prevents actionable decisions from binding without authority.
