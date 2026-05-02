# Governed Workflow Policy Template v0.1

Status: template artefact. No implementation claim. No adoption claim.

## 1. Purpose

This template defines the minimum policy file required for a workflow to qualify as governed under the Consequence Control Stack.

A workflow may only be labelled "governed under this stack" if it satisfies the bundle requirement in Section 3.

## 2. Scope

This template applies to designated governed workflows.

A governed workflow is a workflow explicitly routed through the Consequence Control Stack state model because it can affect external obligations, user-visible behaviour, access, notifications, payments, escalations, queues, safety posture, or audit posture.

## 3. Bundle requirement

A workflow may only claim conformance with the Consequence Control Stack if all three conditions are met:

1. It has a completed governed workflow policy file based on this template.
2. It emits receipts conforming to `RECEIPT_SCHEMA_v0.1.json`.
3. It is covered by at least one adversarial test vector, such as `TEST_VECTOR_PREMATURE_DECISION_v0.1.json`.

If any one of these is missing, the workflow may use the model language but must not claim to be governed under this stack.

## 4. Workflow identity

```text
workflow_id:
workflow_name:
policy_version:
policy_status:
created_at:
updated_at:
```

## 5. Owners

All owner fields are required.

```text
technical_owner:
business_owner:
risk_owner:
bypass_detection_owner:
receipt_registry_owner:
```

Self-ownership alone is not sufficient where validation, risk acceptance, or bypass review is required.

## 6. Inclusion criteria

A workflow must be included if it can alter one or more of:

- external obligations
- user-visible behaviour
- access
- notifications
- payments
- escalations
- queues
- safety posture
- audit posture

```text
included_decision_classes:
included_systems:
included_resources:
included_actors:
```

## 7. Exclusion criteria

Exclusions must be explicit.

```text
excluded_decision_classes:
excluded_systems:
exclusion_reason:
exclusion_owner:
review_date:
```

A workflow must not exclude high-consequence paths without a recorded risk-owner justification.

## 8. Governed resources

Every governed workflow must define resource identifiers.

```text
governed_resource_ids:
resource_owner:
resource_type:
resource_impact:
```

Conflicting `DECISION_READY`, `AUTHORISED`, or `BINDING` decisions against the same governed resource must be detected and recorded.

## 9. Required evidence fields

Every governed workflow must require evidence for:

- risk classification
- affected systems and resources
- alternatives considered
- applicable policy, standard, or control reference
- expected external consequence
- rollback or refusal path

```text
risk_classification:
affected_systems:
affected_resources:
alternatives_considered:
policy_or_standard_reference:
expected_external_consequence:
rollback_or_refusal_path:
supporting_evidence_uri:
```

Missing, invalid, stale, unresolved, or contested evidence prevents entry into `DECISION_READY`.

## 10. Evidence validation rules

Validation must be performed by either:

1. automated checks encoded in the governed workflow; or
2. an approver distinct from the proposer.

Self-validation alone is non-conformant.

```text
validation_method:
automated_checks:
independent_validator:
validation_result:
validation_timestamp:
```

## 11. Evidence currency

Each governed workflow must define maximum evidence age.

```text
maximum_evidence_age:
stale_evidence_response:
revalidation_required:
```

If evidence exceeds its permitted age while `PAUSED`, `DECISION_READY`, or `AUTHORISED`, the decision must re-collect or re-validate evidence before proceeding.

## 12. Pause trigger rules

```text
pause_triggers:
hold_conditions:
release_conditions:
continued_hold_conditions:
release_refusal_conditions:
```

If pause is unresolved, the action must remain `PAUSED` or move to a refusal state.

## 13. Bypass detection

Each governed workflow must define at least one bypass detection mechanism.

Bypass checks must run at least per release or quarterly, whichever occurs first.

```text
bypass_detection_method:
bypass_detection_frequency:
bypass_detection_owner:
bypass_failure_response:
bypass_remediation_status:
```

Detected bypass must be recorded as a separate governed event.

## 14. Receipt requirements

Receipts must conform to `RECEIPT_SCHEMA_v0.1.json`.

Receipts must reference supporting evidence.

Receipts without supporting evidence prove declared process only, not factual prevention.

```text
receipt_schema_version:
receipt_registry:
receipt_registry_owner:
required_receipt_states:
required_evidence_links:
```

## 15. Tamper-evidence

Receipts must be anchored in a tamper-evident store.

Acceptable examples:

- append-only log
- chained hashes using `previous_hash`
- external audit store

```text
tamper_evidence_method:
previous_hash_required:
record_hash_required:
external_anchor_uri:
```

A local `record_hash` alone is not sufficient if the record and hash can both be rewritten without detection.

## 16. State model

Allowed states:

```text
PROPOSED
PAUSED
DECISION_READY
AUTHORISED
BINDING
REVOKED_CANCELLED
HOLD_REFUSED
RELEASE_REFUSED
AUTHORITY_REFUSED
EXECUTION_REFUSED
BYPASS_VIOLATION
```

A state transition is valid only when its entry condition, permitted actions, forbidden actions, and exit condition are recorded.

## 17. Conflict detection

```text
conflict_detection_rule:
conflict_scope:
conflict_response:
conflict_receipt_required:
```

The workflow must detect conflicting decisions against the same governed resource.

The workflow does not need to auto-resolve the conflict, but it must record the conflict as a receipt or governed event.

## 18. Revocation and cancellation

```text
revocation_conditions:
cancellation_conditions:
revocation_required_fields:
cancellation_required_fields:
```

A `PAUSED`, `DECISION_READY`, or `AUTHORISED` item may transition to `REVOKED_CANCELLED` before binding.

Revocation or cancellation must include reason, timestamp, actor, affected resources, and linked prior state.

The same decision instance must not be reused for execution after revocation or cancellation.

## 19. Downstream state checks

For at least one governed workflow, tests must confirm that no downstream state change occurs without a matching `BINDING` receipt.

```text
downstream_systems_checked:
downstream_event_logs:
matching_binding_receipt_required:
downstream_check_frequency:
```

## 20. Claim boundary

This policy file does not prove implementation.

This policy file does not prove adoption.

This policy file does not prove empirical prevention.

It only defines the minimum policy surface required for a workflow to claim governance under the Consequence Control Stack.

## 21. Conformance statement

```text
workflow_id:
policy_version:
receipt_schema_version:
test_vector_reference:
conformance_status:
conformance_date:
approved_by_technical_owner:
approved_by_business_owner:
approved_by_risk_owner:
```

A workflow must not claim conformance unless the policy file, receipt schema, and test vector are all present and linked.
