# Consequence Control Stack

Status: bounded artefact. No implementation. No adoption claim.

## Purpose

Consequence Control Stack defines a bounded control surface for preventing consequence-bearing transitions from becoming binding too early.

Governance fails not only when execution is uncontrolled, but when decision state is reached before readiness, authority, or recovery has resolved.

## Core thesis

Governance only matters where consequence can be stopped.

## Stack shape

Two non-collapsible layers:

1. Consequence Pause Layer
2. Execution Boundary

These layers are related, but not interchangeable.

## Layer 1 — Consequence Pause Layer

### Function

Prevents a response, output, operational proposal, or reaction from becoming decision-ready too early.

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

### Proof surface

- attempted action
- pause trigger condition
- enforced hold duration
- release condition
- non-release evidence

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

## Critical separation

The pause controls whether a decision may become operationally actionable.

The gate controls whether an operationally actionable decision may bind.

These are not the same control.

## Non-execution contexts

This stack is not limited to final execution or deployment.

It also applies where a consequence-bearing commitment can form before execution exists as a concrete queued action, including planning tools, remediation drafts, generated operational instructions, escalation proposals, access-change proposals, and automation-generated workflow changes.

If a proposal can become operationally actionable later, it is in scope before that later execution path appears.

## What normal approval flows may still allow

This stack forbids conditions that ordinary approval workflows may leave open:

- a proposal becoming decision-ready before readiness or authority is resolved
- a parallel shadow decision forming outside the recorded state path
- a blocked decision being recreated through another channel without a linked receipt

## Bypass and coverage

Any path that can alter external obligations, user-visible behaviour, access, notifications, payments, escalations, queues, safety posture, or audit posture is in scope.

Emergency patches, feature flags, shadow deployments, direct database writes, model-triggered workflow calls, manual overrides, and out-of-band messages must either pass through the stack or be recorded as explicit bypass violations.

Bypass is not a configuration choice.

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

Within decisions represented in this stack, it proves the narrower control claim that:

- premature decision state was prevented under the tested condition; and
- unauthorised consequence did not bind under the tested condition.

## Clean line

The pause prevents decisions from becoming actionable too early.

The gate prevents actionable decisions from binding without authority.

## Non-claim boundary

This is not a full runtime.

This is not a replacement for existing governance frameworks.

This is not a claim of institutional adoption, endorsement, or market validation.

This is a bounded artefact defining a two-layer control surface.
