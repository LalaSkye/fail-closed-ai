# Claim Boundary Public Note v0.1

Status: public-claim boundary. No implementation claim. No adoption claim.

## 1. Purpose

This note defines what may and may not be said publicly about the Consequence Control Stack.

It exists to prevent visibility, terminology, or repository activity from being mistaken for implementation, adoption, endorsement, or empirical proof.

## 2. Artefacts in scope

```text
consequence-control-stack/README.md
consequence-control-stack/CONSEQUENCE_CONTROL_STACK_ARTIFACT_v0.1.md
consequence-control-stack/PREMATURE_DECISION_TEST_HARNESS_v0.1.md
consequence-control-stack/GOVERNED_WORKFLOW_POLICY_TEMPLATE_v0.1.md
consequence-control-stack/RECEIPT_SCHEMA_v0.1.json
consequence-control-stack/TEST_VECTOR_PREMATURE_DECISION_v0.1.json
consequence-control-stack/SAMPLE_GOVERNED_WORKFLOW_v0.1.md
consequence-control-stack/TRINITY_FINAL_GATE_v0.1.md
```

## 3. Current evidence status

The current stack contains:

- bounded design artefact
- test-harness specification
- governed workflow policy template
- machine-readable receipt schema
- replayable premature-decision test vector
- sample governed workflow
- final gate receipt

The current stack does not contain:

- runtime implementation
- executed test run
- deployment evidence
- institutional adoption
- external endorsement
- empirical proof of prevention

## 4. Allowed public claim

Allowed wording:

```text
The Consequence Control Stack is a bounded design and inspection artefact for testing whether governed workflows prevent consequence-producing actions from becoming decision-ready before required evidence, pause resolution, and authority checks have completed.
```

Also allowed:

```text
This is a design artefact, receipt schema, and test-vector surface.
It is not a runtime implementation claim.
```

Also allowed:

```text
The current proof surface is artefact-level: policy template, receipt schema, test vector, sample workflow, and claim-boundary note.
```

## 5. Forbidden public claims

Do not claim:

- implemented runtime
- deployed system
- organisational adoption
- partner validation
- institutional endorsement
- market proof
- empirical prevention
- production guarantee
- compliance guarantee
- safety guarantee
- proof that premature decisions are reduced in real systems
- proof that all bypass paths are blocked
- proof that human decisions are correct

## 6. Required qualifiers

Any public reference must include one of the following qualifiers:

```text
Design artefact only.
```

```text
No implementation claim.
```

```text
No deployment evidence yet.
```

```text
Artefact-level proof surface only.
```

## 7. Claim boundary

The stack may claim to define an inspectable control surface.

The stack may not claim to prove operational prevention without executable tests and deployment evidence.

The stack may claim a replayable test shape.

The stack may not claim that the test has been executed unless a run receipt exists.

The stack may claim a receipt schema.

The stack may not claim factual prevention from a receipt alone unless the receipt links to supporting evidence.

## 8. Public positioning rule

Use language close to:

- bounded design artefact
- governed workflow
- decision-ready state
- proof surface
- receipt schema
- test vector
- claim limit
- no implementation claim
- no adoption claim

Avoid language close to:

- revolution
- breakthrough
- new paradigm
- solved governance
- proven runtime
- market validation
- industry adoption
- endorsement
- production-ready
- universal layer

## 9. Comparison boundary

Do not position this as replacing runtime governance, change control, risk management, legal review, or human oversight.

Permitted comparison:

```text
Runtime controls ask whether an action may execute.
This artefact asks whether a governed workflow allowed the action to become decision-ready too early.
```

Forbidden comparison:

```text
This replaces existing governance systems.
```

Forbidden comparison:

```text
This proves other runtime governance approaches are incomplete.
```

## 10. Public post gate

Before any public post, check:

1. Does the post make clear this is design/test artefact only?
2. Does the post avoid implementation or adoption claims?
3. Does the post keep the claim smaller than the evidence?
4. Does the post point to the artefact bundle rather than social validation?
5. Does the post stop cleanly without inviting category fights?

If any answer is no, do not post.

## 11. Approved short description

```text
Consequence Control Stack is a design artefact for inspecting whether a governed workflow allows a consequence-producing action to become decision-ready before required evidence, pause resolution, and authority checks are complete.

Current status: artefact-level only — policy template, receipt schema, test vector, sample workflow, and claim boundary. No runtime implementation or deployment claim.
```

## 12. Clean stop

If a public statement requires stronger claims than this note allows, the statement must not be made.

The artefact can be shown.

It must not be inflated.
