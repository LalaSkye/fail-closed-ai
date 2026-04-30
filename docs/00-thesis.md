# Thesis

Fail-closed AI is the discipline of designing AI-controlled systems so invalid action paths cannot become consequence.

The claim is not that AI systems can be made perfect.

The claim is narrower:

> When an AI-controlled action reaches a consequence-producing boundary, the system must require proof before execution.

If proof is missing, stale, out of scope, replayed, or unauthorised, the system stops.

It does not continue optimistically.

It holds.

---

## Why this matters

Many governance systems operate after the fact:

- review
- audit
- reporting
- explanation
- escalation
- policy language

These are useful, but they are not the same as control.

Control exists where an invalid transition cannot execute.

---

## Core question

> Where does the system physically stop?

If that question cannot be answered, the governance boundary is not yet engineered.

---

## Minimal requirement

A fail-closed AI system must show:

1. what action was attempted
2. what authority was required
3. which proof was missing or invalid
4. where execution stopped
5. whether consequence occurred
6. what receipt was written

No receipt, no proof.

No proof, no transition.
