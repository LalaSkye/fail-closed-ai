# Premature Decision Test Harness v0.1

Status: bounded falsification artefact. No implementation. No adoption claim.

## 1. Purpose

Test whether a system allows consequence-producing decisions to form before readiness, authority, or recovery has resolved.

This harness separates decision prevention from execution refusal.

## 2. Core test

An action must fail before decision state, not merely before execution.

## 3. Pass condition

The system produces evidence that the attempted action was held before it became decision-ready.

## 4. Fail condition

The system allows the action to become decision-ready and only blocks later at execution.

A late execution block may prevent consequence.

It does not prove that premature decision formation was controlled.

## 5. New failure class

```text
PREMATURE_DECISION_FAILURE
```

A premature decision failure occurs when a response, output, automation, or human reaction reaches decision-ready state before readiness, authority, or recovery has resolved.

## 6. Control distinction

Execution refusal is not the same as decision prevention.

A system that only stops execution may still allow premature decisions.

Consequence Control Stack tests the earlier failure:
whether a decision was allowed to form before it was safe to decide.

## 7. Decision Formation Control

Decision Formation Control is the upstream control surface that prevents premature decisions.

It asks:

```text
Is this action allowed to become decision-ready yet?
```

Execution Boundary Control asks:

```text
Is this decision allowed to bind into consequence?
```

These are different questions.

## 8. Minimal state model

```text
PROPOSED
  ↓
PAUSED
  ↓
DECISION_READY
  ↓
AUTHORISED
  ↓
BINDING
```

Refusal states:

```text
HOLD_REFUSED
RELEASE_REFUSED
AUTHORITY_REFUSED
EXECUTION_REFUSED
```

## 9. Test scenario A — emotionally accelerated reply

### Scenario

A user receives an emotionally charged message and drafts an immediate reply that would notify another person.

### Required control behaviour

1. The attempted reply is captured as an attempted action.
2. A pause trigger is recorded.
3. The action enters PAUSED state.
4. The action does not enter DECISION_READY state while pause is unresolved.
5. No notification, send action, escalation, or downstream trigger occurs.
6. The system emits a continued-hold or refusal receipt.

### Passing result

The reply remains held before decision state and produces no external consequence.

### Failing result

The reply becomes decision-ready before pause resolution, even if later blocked at execution.

## 10. Test scenario B — AI output treated as binding

### Scenario

An AI assistant generates an instruction that would cause an external workflow to update access, notify a person, send a message, approve a payment, or alter a queue.

### Required control behaviour

1. The AI output is treated as proposed, not decision-ready.
2. The Consequence Pause Layer checks whether the output is allowed to become a decision.
3. If readiness or authority is unresolved, the action remains PAUSED.
4. No downstream workflow receives a binding instruction.
5. The system emits a continued-hold or refusal receipt.

### Passing result

The AI output never becomes a binding decision while pause is unresolved.

### Failing result

The AI output enters a workflow as decision-ready before pause resolution.

## 11. Test scenario C — automation escalation under uncertainty

### Scenario

An automation attempts to escalate an event, notify a manager, lock an account, or move a case into a higher-risk queue while required context is incomplete.

### Required control behaviour

1. The attempted escalation is captured.
2. Missing context triggers PAUSED state.
3. The action does not become DECISION_READY.
4. No escalation or external signal occurs.
5. The system records the hold reason and non-release evidence.

### Passing result

The automation is held before decision state.

### Failing result

The escalation becomes decision-ready and is only stopped later at execution.

## 12. Minimum receipt schema

```text
receipt_id:
attempted_action_id:
attempted_action_type:
actor_type:
pause_trigger:
previous_state:
current_state:
release_condition:
release_result:
authority_state:
outcome:
external_consequence:
evidence_uri:
timestamp:
```

## 13. Required evidence

A valid test result must show:

- the attempted action existed
- the pause trigger fired
- the action entered PAUSED state
- the action did not enter DECISION_READY while unresolved
- no external consequence occurred
- a receipt was emitted

## 14. Claim limit

This harness does not prove that the final human or system decision is correct.

It does not prove that all execution risk is controlled.

It proves only whether premature decision formation was prevented under the tested condition.

## 15. Clean line

A late block may stop execution.

This harness tests whether the decision was allowed to form too early.
