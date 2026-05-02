# Sample Governed Workflow v0.1

Status: worked example only. No implementation claim. No adoption claim.

## 1. Purpose

This sample shows how a governed workflow applies the Consequence Control Stack bundle:

1. governed workflow policy
2. receipt schema
3. adversarial test vector

The example uses an emotionally accelerated reply that would create an external message and recipient notification.

## 2. Claim boundary

This sample does not prove implementation.

This sample does not prove adoption.

This sample does not prove empirical prevention.

It only shows how the artefacts connect for one governed workflow example.

## 3. Artefact bundle

A workflow may only claim to be governed under this stack if all three artefacts are present and linked:

```text
policy template:
GOVERNED_WORKFLOW_POLICY_TEMPLATE_v0.1.md

receipt schema:
RECEIPT_SCHEMA_v0.1.json

test vector:
TEST_VECTOR_PREMATURE_DECISION_v0.1.json
```

If any artefact is missing, the workflow may use the model language but must not claim conformance.

## 4. Workflow identity

```text
workflow_id: gwf-emotional-reply-review-001
workflow_name: Emotionally Accelerated Reply Review
policy_version: 0.1
policy_status: sample_only
```

## 5. Owners

```text
technical_owner: example_technical_owner
business_owner: example_business_owner
risk_owner: example_risk_owner
bypass_detection_owner: example_bypass_detection_owner
receipt_registry_owner: example_receipt_registry_owner
```

All owner fields are required in a real governed workflow.

## 6. Governed scope

This workflow covers attempted actions that may cause:

- external message send
- recipient notification
- escalation message
- queue mutation
- downstream workflow trigger

Governed systems:

```text
example_messaging_system
example_notification_queue
```

Governed resource identifiers:

```text
resource:message-send-queue
resource:recipient-notification-channel
```

## 7. Scenario

A user receives an emotionally charged message and drafts an immediate reply.

The reply would notify another person if sent.

The attempted action is therefore consequence-producing.

## 8. Initial attempted action

```text
attempted_action_id: attempt-emotional-reply-001
attempted_action_type: external_message_send
actor_type: human
initiator_identity: example_user
initial_state: PROPOSED
proposed_external_consequence: recipient_message_and_notification
```

## 9. Pause trigger

```text
pause_trigger: emotional_acceleration_with_external_notification_consequence
triggered: true
required_result: PAUSED
```

The action must not enter `DECISION_READY` while pause is unresolved.

## 10. Required evidence check

Minimum required evidence fields:

```text
risk_classification: missing
affected_systems_and_resources: present
alternatives_considered: missing
policy_or_standard_reference: missing
expected_external_consequence: present
rollback_or_refusal_path: missing
```

Because required evidence is missing, the action must remain `PAUSED` or move to a refusal state.

It must not enter `DECISION_READY`.

## 11. Expected state path

Allowed path:

```text
PROPOSED → PAUSED
```

Forbidden path while pause is unresolved:

```text
DECISION_READY
AUTHORISED
BINDING
```

## 12. Expected receipt behaviour

The workflow must emit a receipt conforming to:

```text
RECEIPT_SCHEMA_v0.1.json
```

The receipt must include:

- workflow policy reference
- policy version
- owners
- governed resource IDs
- pause trigger
- previous state
- current state
- required evidence fields
- evidence validation result
- evidence currency result
- release result
- conflict check result
- downstream state check
- bypass check result
- evidence URI
- previous_hash
- record_hash
- tamper-evidence store

A receipt without linked supporting evidence proves declared process only, not factual prevention.

## 13. Expected receipt surface

Expected receipt outcome:

```text
previous_state: PROPOSED
current_state: PAUSED
release_result: continued_hold
outcome: paused
external_consequence.occurred: false
downstream_state_check.performed: true
downstream_state_check.result: no_downstream_change
bypass_check_result.performed: true
bypass_check_result.result: no_bypass_detected
```

## 14. Downstream state check

The workflow must check that no downstream state change occurred without a matching `BINDING` receipt.

For this sample:

```text
checked_systems:
- example_messaging_system
- example_notification_queue

required_result:
no_downstream_change
```

Any message send, notification, escalation, queue mutation, or downstream trigger while the action is `PAUSED` fails the workflow.

## 15. Bypass check

The workflow must check for bypass attempts.

Example bypass detection method:

```text
compare_message_send_queue_and_notification_event_log_against_binding_receipts
```

Required result:

```text
no_bypass_detected
```

If a downstream consequence occurred without a matching `BINDING` receipt, the result must be `BYPASS_VIOLATION`.

## 16. Test vector link

This sample is tested by:

```text
TEST_VECTOR_PREMATURE_DECISION_v0.1.json
```

The test vector must fail if:

- the policy file reference is missing
- the receipt does not validate against `RECEIPT_SCHEMA_v0.1.json`
- any required receipt field is missing
- evidence validation is `not_performed`
- self-validation is true
- downstream state check is not performed
- bypass check is not performed
- the action enters `DECISION_READY` while evidence is missing
- the action enters `AUTHORISED` or `BINDING` while pause is unresolved
- external consequence occurs while current state is `PAUSED`

## 17. Pass condition

The sample passes only if:

```text
attempted_action exists
pause_trigger fires
current_state remains PAUSED
DECISION_READY is not reached
AUTHORISED is not reached
BINDING is not reached
no external consequence occurs
schema-valid receipt is emitted
supporting evidence is linked
downstream state check is performed
bypass check is performed
```

## 18. Fail condition

The sample fails if:

```text
message is sent
recipient is notified
queue is mutated
external escalation occurs
DECISION_READY is reached while required evidence is missing
AUTHORISED is reached while pause is unresolved
BINDING is reached without valid authority
receipt is missing
receipt is schema-invalid
receipt lacks evidence URI
downstream check is missing
bypass check is missing
```

## 19. Clean judgement

This sample demonstrates the inspection path:

```text
policy → schema → test vector → receipt → downstream check
```

It does not demonstrate runtime implementation.

It does not demonstrate empirical prevention.

It gives one concrete shape for testing premature decision prevention inside a governed workflow.
