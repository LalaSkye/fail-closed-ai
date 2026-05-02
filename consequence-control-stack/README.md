# Consequence Control Stack

Status: bounded artefact. No implementation. No adoption claim.

## Purpose

Consequence Control Stack defines a bounded control surface for preventing consequence-bearing transitions from becoming binding too early within governed workflows.

Governance fails not only when execution is uncontrolled, but when decision-ready state is reached before readiness, authority, or recovery has resolved.

Current status: design and test harness only. No canonical runtime implementation is shipped with this version.

## Core thesis

Governance only matters where consequence can be stopped.

## Scope

This stack applies to designated governed workflows.

A governed workflow is any workflow explicitly routed through this state model because it can affect external obligations, user-visible behaviour, access, notifications, payments, escalations, queues, safety posture, or audit posture.

Extension beyond governed workflows is optional.

Claims in this artefact apply only to decisions represented in this stack.

## Stack shape

Two non-collapsible layers:

1. Consequence Pause Layer
2. Execution Boundary

These layers are related, but not interchangeable.

## Layer 1 — Consequence Pause Layer

### Function

Prevents a response, output, operational proposal, or reaction from becoming decision-ready too early inside a governed workflow.

### Invariant

No consequence-producing action may enter decision-ready state while pause is unresolved.

### Mechanism

```text
attempted action
→ pause trigger
→ enforced hold
→ readiness / authority pre-check
→ release to decision OR continued hold
```

### Boundary

The system physically stops before a decision becomes operationally actionable.

### Decision-ready definition

`DECISION_READY` means all required evidentiary fields are present and validated.

If any required field is missing, invalid, unresolved, or contested, the action must remain `PAUSED` or move to a refusal state.

### Operationally actionable definition

A decision is operationally actionable when it contains enough specific detail to trigger a change in code, configuration, data, access, workflow state, notification, payment, escalation, obligation, or external instruction without new design choices.

### Proof surface

- attempted action
- pause trigger condition
- enforced hold duration
- release condition
- non-release evidence
- supporting evidence URI

### Failure addressed

- reaction becomes decision under pressure
- AI output is treated as decision-ready
- human commits before recovery
- automation escalates without stabilisation

## Layer 2 — Execution Boundary

### Function

Determines whether a decision may bind into consequence.

### Invariant

No state mutation without valid authority at execution.

### Mechanism

```text
decision-ready action
→ authority verification
→ allow / refuse / escalate
→ execution or block
```

### Boundary

The system physically stops before consequence binds.

### Proof surface

- authority verification
- decision outcome
- execution or refusal trace
- audit receipt
- downstream state check where applicable

## Critical separation

The pause controls whether a decision may become operationally actionable.

The gate controls whether an operationally actionable decision may bind.

These are not the same control.

## Non-execution contexts

This stack is not limited to final execution or deployment.

Within governed workflows, it also applies where a consequence-bearing commitment can form before execution exists as a concrete queued action, including planning tools, remediation drafts, generated operational instructions, escalation proposals, access-change proposals, and automation-generated workflow changes.

If a proposal can become operationally actionable later, it is in scope before that later execution path appears.

## What normal approval flows may still allow

This stack forbids conditions that ordinary approval workflows may leave open:

- a proposal becoming decision-ready before required evidence is present and validated
- a parallel shadow decision forming outside the recorded state path
- a blocked decision being recreated through another channel without a linked receipt
- a downstream change occurring without a matching `BINDING` receipt in a governed workflow

## Bypass and coverage

A minimal deployment may start with one governed workflow and a single receipt registry.

Broader coverage is incremental, not required for this artefact.

Within a governed workflow, emergency patches, feature flags, shadow deployments, direct database writes, model-triggered workflow calls, manual overrides, and out-of-band messages must either pass through the stack or be recorded as explicit bypass violations.

Implementers must define at least one bypass detection mechanism, such as periodic trace comparison between downstream event logs and stack receipts.

A detected bypass is a separate governed event.

Bypass is not a configuration choice within governed workflows.

Bypass is a failed control.

## Relation to existing governance

This does not replace threat modelling, change control, runtime policy enforcement, legal review, or human oversight.

It sits beside them as a state-control surface for when decisions may become operationally actionable and when they may bind.

Runtime controls answer whether an action may execute.

This stack also asks whether the decision was allowed to become actionable in the first place.

## Primary failure class

Premature decision.

A premature decision occurs when a response, output, automation, or human reaction reaches decision-ready state before readiness, authority, or recovery has resolved.

## Claim limit

This artefact does not prove that a decision is correct.

Within governed workflows and decisions represented in this stack, it proves the narrower control claim that:

- premature decision state was prevented under the tested condition; and
- unauthorised consequence did not bind under the tested condition.

Demonstrating broader reductions in premature decision formation requires deployment evidence not included here.

A receipt alone does not prove factual prevention unless it links to supporting evidence, such as blocked transition logs, negative downstream checks, or refusal traces.

## Clean line

The pause prevents decisions from becoming actionable too early.

The gate prevents actionable decisions from binding without authority.

## Non-claim boundary

This is not a full runtime.

This is not a replacement for existing governance frameworks.

This is not a claim of institutional adoption, endorsement, or market validation.

This is a bounded artefact defining a two-layer control surface.
