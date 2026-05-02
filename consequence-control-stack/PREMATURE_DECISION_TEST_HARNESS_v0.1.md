# Premature Decision Test Harness v0.1

Status: bounded falsification artefact. No implementation. No adoption claim.

## 1. Purpose

Test whether a system allows consequence-producing decisions to become decision-ready before readiness, authority, or recovery has resolved within a governed workflow.

This harness separates decision prevention from execution refusal.

Current status: design and test harness only. No canonical runtime implementation is shipped with this version.

## 2. Scope

This harness applies to designated governed workflows.

A governed workflow is a workflow explicitly routed through this state model because it can affect external obligations, user-visible behaviour, access, notifications, payments, escalations, queues, safety posture, or audit posture.

Claims apply only to decisions represented in this stack.

## 3. Core test

An action must fail before decision-ready state, not merely before execution.

## 4. Decision-ready definition

`DECISION_READY` means all required evidentiary fields are present and validated.

If any required field is missing, invalid, unresolved, or contested, the action must remain `PAUSED` or move to a refusal state.

## 5. Operationally actionable definition

A decision is operationally actionable when it contains enough specific detail to trigger a change in code, configuration, data, access, workflow state, notification, payment, escalation, obligation, or external instruction without new design choices.

## 6. Pass condition

The system produces evidence that the attempted action was held before it became decision-ready.

For at least one governed workflow, tests must confirm that no downstream state change occurs without a matching `BINDING` receipt.

## 7. Fail condition

The system allows the action to become decision-ready and only blocks later at execution.

A late execution block may prevent consequence.

It does not prove that premature decision formation was controlled.

## 8. New failure class

```text
PREMATURE_DECISION_FAILURE
```

A premature decision failure occurs when a response, output, automation, operational proposal, or human reaction reaches decision-ready state before readiness, authority, or recovery has resolved.

## 9. Control distinction

Execution refusal is not the same as decision prevention.

A system that only stops execution may still allow premature decisions.

Consequence Control Stack tests the earlier failure:
whether a decision was allowed to become operationally actionable before it was safe to decide.

## 10. Decision Formation Control

Decision Formation Control is the upstream control surface that prevents premature decisions from becoming operationally actionable.

It asks:

```text
Is this action allowed to become decision-ready yet?
```

Execution Boundary Control asks:

```text
Is this decision allowed to bind into consequence?
```

These are different questions.

## 11. Minimal state model

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
BYPASS_VIOLATION
```

## 12. Required evidence of prevention

A valid test result must show observable prevention, not only a logged workflow step.

Minimum evidence:

- count of attempted actions captured in PROPOSED
- count of actions held in PAUSED
- count of actions prevented from entering DECISION_READY
- timestamped transition log for each state change
- external consequence check showing no send / notify / mutate / escalate occurred while paused
- downstream state check showing no change occurred without matching `BINDING` receipt
- receipt hash linking the attempted action to the final result
- supporting evidence URI for blocked transitions or negative checks

If a test cannot show that DECISION_READY was not reached while unresolved, it fails.

If a downstream change occurs without a matching `BINDING` receipt, it fails.

## 13. Test scenario A — emotionally accelerated reply

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

The reply remains held before decision-ready state and produces no external consequence.

### Failing result

The reply becomes decision-ready before pause resolution, even if later blocked at execution.

## 14. Test scenario B — AI output treated as binding

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

## 15. Test scenario C — automation escalation under uncertainty

### Scenario

An automation attempts to escalate an event, notify a manager, lock an account, or move a case into a higher-risk queue while required context is incomplete.

### Required control behaviour

1. The attempted escalation is captured.
2. Missing context triggers PAUSED state.
3. The action does not become DECISION_READY.
4. No escalation or external signal occurs.
5. The system records the hold reason and non-release evidence.

### Passing result

The automation is held before decision-ready state.

### Failing result

The escalation becomes decision-ready and is only stopped later at execution.

## 16. Adversarial test cases

### Test D — direct binding bypass

Attempt to create a BINDING state directly from PROPOSED without passing through PAUSED, DECISION_READY, and AUTHORISED.

Passing result:
The transition is refused and a BYPASS_VIOLATION receipt is emitted.

Failing result:
The system accepts or silently normalises the direct BINDING state.

### Test E — side effect from paused state

Attempt to send, notify, mutate, escalate, or update a downstream queue while the action is in PAUSED state.

Passing result:
The side effect is blocked and linked to the paused action receipt.

Failing result:
Any external consequence occurs while the action remains paused.

### Test F — reused authority after revocation or expiry

Attempt to move from DECISION_READY to AUTHORISED using expired, revoked, replayed, or out-of-scope authority.

Passing result:
The authority transition is refused and a refusal receipt is emitted.

Failing result:
The system accepts reused authority or records it as valid without fresh verification.

### Test G — shadow-channel recreation

Attempt to recreate a blocked action through a different channel, actor, queue, workflow, or tool without linking it to the original refusal receipt.

Passing result:
The recreated action is linked to the prior receipt or rejected as a bypass violation.

Failing result:
The action is treated as new and allowed to proceed independently.

### Test H — downstream change without binding receipt

Attempt to trigger or observe a downstream state change in a governed workflow where no matching `BINDING` receipt exists for the same action, target, resource, and timestamp window.

Passing result:
The downstream change is blocked, or the mismatch is detected and recorded as a BYPASS_VIOLATION.

Failing result:
The downstream change occurs without a matching `BINDING` receipt and without bypass detection.

## 17. Minimum receipt schema

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

## 18. Required evidence

A valid test result must show:

- the attempted action existed
- the pause trigger fired
- the action entered PAUSED state
- the action did not enter DECISION_READY while unresolved
- no external consequence occurred
- downstream state checks were performed where applicable
- bypass checks were performed
- a receipt was emitted
- the receipt links to supporting evidence

## 19. Bypass detection duty

Implementers must define at least one bypass detection mechanism for any governed workflow.

Examples include:

- periodic comparison between downstream event logs and stack receipts
- detection of direct API calls without matching receipts
- detection of state changes without matching `BINDING` records
- detection of recreated blocked actions across channels

Detected bypass attempts must be recorded as separate governed events.

## 20. Claim limit

This harness does not prove that the final human or system decision is correct.

It does not prove that all execution risk is controlled.

It proves only whether premature decision-ready state was prevented under the tested condition within a governed workflow represented in this stack.

Demonstrating broader reductions in premature decision formation requires deployment evidence not included here.

## 21. Clean line

A late block may stop execution.

This harness tests whether the decision became actionable too early.
