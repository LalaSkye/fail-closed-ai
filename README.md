# Fail-Closed AI

**Reference architecture for AI systems that stop before unsafe consequence.**

Most AI governance tells systems what they should not do.

Fail-closed AI makes invalid action paths unable to execute.

The core question is simple:

> **Where does the system physically stop?**

---

## Core invariant

No AI-controlled action may become consequence unless the transition is:

- admissible
- authorised
- scoped
- fresh
- unreplayed
- receipt-bearing

If any check fails, the system does not continue.

It holds.

---

## Governance corridor

```text
proposal
  |
interpretation admissibility
  |
authority check
  |
DecisionRecord
  |
commit gate
  |
execution boundary
  |
consequence
  |
receipt
```

The corridor exists to prevent invalid transitions from becoming real-world effects.

A policy may describe a rule.

A fail-closed system must enforce the boundary.

---

## Minimal proof shape

A useful fail-closed AI system must show:

1. what action was attempted
2. what authority was required
3. which proof was missing or invalid
4. where execution stopped
5. whether consequence occurred
6. what receipt was written

Example:

```text
Attempt:        send external email
DecisionRecord: missing authority
Verdict:        HOLD
Email sent:     false
Receipt written: true
```

That is the difference between governance commentary and runtime control.

---

## Verdicts

| Verdict | Meaning |
|---|---|
| `ALLOW` | The transition is admissible and may execute. |
| `HOLD` | The transition cannot be validated. Execution stops. |
| `DENY` | The transition is invalid or prohibited. Execution stops. |

Ambiguity is not permission.

---

## Related kernel

The first working kernel is here:

[`commit-gate-core`](https://github.com/LalaSkye/commit-gate-core)

That repo demonstrates one narrow invariant:

> No state mutation without a valid `DecisionRecord`.

This repository is the wider reference architecture around that kernel.

---

## Repository map

```text
fail-closed-ai/
├── README.md
├── docs/
│   ├── 00-thesis.md
│   ├── 01-governance-corridor.md
│   ├── 02-decision-record.md
│   ├── 03-admissibility.md
│   ├── 04-commit-boundary.md
│   ├── 05-execution-boundary.md
│   ├── 06-receipts.md
│   └── 07-threat-model.md
├── reference/
│   ├── decision_record.schema.json
│   ├── receipt.schema.json
│   └── verdicts.md
└── examples/
    └── unsafe-email-send.md
```

The initial public surface is documentation-first.

Code can follow only where the boundary is already clear.

---

## Boundary

This repository does not claim that every AI risk can be solved by one gate.

It claims something narrower and more testable:

> An AI-controlled action should not become consequence unless the required proof is present at the boundary where consequence occurs.

That claim can be inspected.

That claim can be tested.

That claim can fail.

Good. That is what makes it engineering.

---

## What this does not prove

This repository does not prove adoption, certification, standardisation, or production readiness.

It demonstrates a bounded execution-control surface that can be run, inspected, and tested.

---

## Design principles

- Stop is a first-class primitive.
- Authority is checked before mutation.
- Ambiguity fails closed.
- Receipts are written for refusal, not just success.
- Tests must prove bypass failure, not only happy paths.
- Claims must be no larger than the evidence can carry.

---

## Status

`v0.1` — canonical anchor established.

Next work:

- define the governance corridor
- define `DecisionRecord`
- define receipt structure
- define threat model
- add runnable examples

---

## Licence

MIT.

Use it. Break it. Show the receipt.
