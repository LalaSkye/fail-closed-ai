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

## 4. Layer model

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

## 5. Layer 1 — Consequence Pause Layer

### Purpose

Prevent a response, AI output, automation, operational proposal, or human reaction from becoming decision-ready before readiness has resolved.

### Invariant

No consequence-producing action may enter decision-ready state while pause is unresolved.

### Stop point

The system physically stops before a decision becomes operationally actionable.

### Decision-ready definition

`DECISION_READY` means all required evidentiary fields are present and validated.

If any required field is missing, invalid, unresolved, or contested, the action must remain `PAUSED` or move to a refusal state.

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

## 6. Layer 2 — Execution Boundary

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

## 7. State model requirements

States must be mutually exclusive for a given attempted action.

A state transition is valid only when its entry condition, permitted actions, forbidden actions, and exit condition are recorded.

| State | Entry condition | Permitted actions | Forbidden actions | Exit condition |
|---|---|---|---|---|
| PROPOSED | An actor or system creates an attempted action record. | Record intent, classify action type, evaluate pause trigger. | Send, notify, escalate, mutate state, create external obligation, mark as approved. | Pause trigger evaluated. |
| PAUSED | Pause trigger fires or readiness/authority/recovery is unresolved. | Hold, gather context, request authority, continue hold, refuse release. | Enter execution queue, notify external party, mutate state, create binding instruction. | Release condition satisfied or release refused. |
| DECISION_READY | Required evidentiary fields are present, validated, and linked to the action record. | Submit for authority verification, attach evidence, request approval. | Bind, execute, reuse prior authority without verification. | Authority allowed, refused, or escalated. |
| AUTHORISED | Valid scoped authority is verified for the exact action. | Execute within scope, record authorisation, prepare audit receipt. | Execute outside scope, replay authority, alter target/action without new authority. | Execution completed, refused, expired, or revoked. |
| BINDING | Consequence-producing transition has executed under valid authority. | Record final trace, emit audit receipt, link evidence. | Modify receipt silently, erase prior states, hide bypass path. | Final receipt emitted. |

## 8. Mandatory coverage

A minimal deployment may start with one governed workflow and a single receipt registry.

Broader coverage is incremental, not required for this artefact.

Within a governed workflow, emergency changes, feature flags, shadow deployments, direct database writes, model-triggered workflow calls, manual overrides, and out-of-band messages must either pass through the stack or be recorded as bypass violations.

Implementers must define at least one bypass detection mechanism, such as periodic trace comparison between downstream event logs and stack receipts.

A detected bypass is a separate governed event.

## 9. Failure class

### Premature decision

A premature decision occurs when a response, output, automation, operational proposal, or human reaction reaches decision-ready state before readiness, authority, or recovery has resolved.

This is distinct from unauthorised execution.

Premature decision happens before the execution gate.

## 10. Minimum failure test

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

## 11. Proof surface

A valid artefact must show:

- attempted action
- pause trigger
- hold state
- resolution or continued hold
- state transition evidence
- supporting evidence URI
- authority check where applicable
- allow / refuse / escalate outcome
- execution or non-execution trace
- audit receipt
- bypass check result
- downstream state check where applicable

## 12. Minimum receipt fields

```text
receipt_id:
decision_id:
attempted_action_id:
attempted_action_type:
initiator_identity:
actor_type:
reviewer_identity:
affected_systems:
affected_resources:
pause_trigger:
previous_state:
current_state:
state_transition_timestamp:
required_evidence_fields:
evidence_validation_result:
release_condition:
release_result:
authority_state:
authority_scope:
authority_expiry:
authority_revocation_status:
override_status:
contested_status:
outcome:
external_consequence:
downstream_state_check:
bypass_check_result:
evidence_uri:
record_hash:
timestamp:
```

Receipts attest to process and must reference supporting evidence.

A receipt without linked evidence only proves declared process, not factual prevention.

## 13. Claim limit

This artefact does not prove that a human decision is correct.

It does not prove that all governance risk is solved.

It proves a narrower control claim within governed workflows and decisions represented in this stack:

- premature decision-ready state was prevented under the tested condition; and
- unauthorised consequence did not bind under the tested condition.

Demonstrating broader reductions in premature decision formation requires deployment evidence not included here.

## 14. Non-claim boundary

This is not a full runtime.

This is not a product claim.

This is not an endorsement, adoption, partnership, or market-validation claim.

This is a bounded control artefact for inspection.

## 15. Clean line

The pause prevents decisions from becoming actionable too early.

The gate prevents actionable decisions from binding without authority.
