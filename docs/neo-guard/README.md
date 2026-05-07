# NEO Guard — Human Node Admissibility Layer

**Status:** v0.1 runnable end-to-end proof surface  
**Scope:** human override / human authorization admissibility before consequence binding  
**Parent frame:** TrinityOS / fail-closed AI / consequence control

## Core claim

```text
The human node is inside the geometry, not above it.
```

NEO Guard protects an execution-governed system from the human operator becoming the bypass.

It does not claim humans are safe. It makes human override inspectable before consequence binds.

## Problem

Many AI governance systems control model output but quietly trust the human override path.

That leaves a structural gap:

```text
AI output is governed
human override is treated as authority
consequence binds
no proof that the human-node state was admissible
```

NEO Guard addresses that gap.

## Position in the stack

```text
model_output
   ↓
governance_layer
   ↓
NEO Guard
   ↓
CommitGate / execution boundary
   ↓
execution | refusal
```

NEO Guard sits before CommitGate when a human operator attempts to authorize, escalate, release, or override a consequence-bearing action.

## Core invariant

```text
No stable operator standing → no authority elevation.
No authority elevation → no override.
No override → no bypassed consequence.
```

## What NEO Guard checks

| Check | Purpose |
|---|---|
| Operator identity | Who is trying to bind consequence? |
| Authority scope | Is the role allowed to authorize this action? |
| Consequence class | How serious is the downstream effect? |
| Override request | Is the operator trying to bypass a prior refusal or hold? |
| State signal | Is the operator state stable enough for authority elevation? |
| Pressure signals | Is the action rushed, repeated, defensive, or overloaded? |
| Reason | Is there an inspectable basis for override? |

## Outcomes

```text
ALLOW
HOLD
ESCALATE
REFUSE
HALT
```

Only `ALLOW` may continue toward CommitGate.

All other outcomes deny authority elevation and emit a receipt.

## Proof layers

### 1. Operator-standing resolver

```text
human-node request
→ NEO Guard outcome
→ authority elevation allowed / blocked
→ receipt hash
```

### 2. NEO Guard → CommitGate chain receipt

```text
NEO Guard outcome
→ CommitGate eligibility
→ COMMIT_GATE_ELIGIBLE | COMMIT_GATE_NOT_CALLED
→ chain receipt hash
```

### 3. End-to-end proof path

```text
NEO Guard
→ CommitGate eligibility
→ bounded mock CommitGate decision
→ final receipt
```

Covered paths:

| Path | Final result |
|---|---|
| NEO Guard blocks upstream | `REFUSE` / `NO_DOWNSTREAM_EXECUTION_ATTEMPT` |
| NEO Guard allows; CommitGate refuses | `REFUSE` / `COMMIT_REFUSED_NO_EFFECT` |
| NEO Guard allows; CommitGate executes | `EXECUTE` / `COMMIT_ALLOWED` |

## Run locally

From this folder:

```bash
cd docs/neo-guard
python run_demo.py
python run_chain_demo.py
python run_end_to_end_demo.py
pytest
```

## CI proof surface

GitHub Actions workflow:

```text
.github/workflows/neo-guard-tests.yml
```

The workflow runs:

```text
pytest
python run_end_to_end_demo.py
```

on changes to `docs/neo-guard/**`.

## Files

- `neo_guard/guard.py` — deterministic operator-standing resolver
- `neo_guard/chain.py` — NEO Guard → CommitGate eligibility chain receipt
- `neo_guard/commit_gate.py` — bounded mock CommitGate for proof-path testing
- `neo_guard/end_to_end.py` — final NEO Guard → CommitGate proof flow
- `neo_guard/models.py` — request / response models
- `neo_guard/receipts.py` — canonical SHA-256 receipt hashing
- `examples/override_attempt_blocked.json` — example blocked override
- `tests/test_neo_guard.py` — operator-standing tests
- `tests/test_chain.py` — CommitGate eligibility chain tests
- `tests/test_end_to_end.py` — final proof-path tests
- `SPEC_v0.1.md` — design specification
- `CHAIN_RECEIPT_v0.1.md` — chain receipt proof note
- `END_TO_END_PROOF_v0.1.md` — end-to-end proof note
- `CLAIM_BOUNDARY_v0.1.md` — public claim limits

## What this does not prove

This does not prove:

- humans are safe
- emotion can be measured clinically
- all bad overrides are prevented
- this is a production deployment
- this replaces CommitGate
- this is a certification claim
- this is externally audited

It proves only a bounded mechanism:

```text
human override can be intercepted, evaluated, blocked, and receipted before consequence binds
```

and:

```text
human-node admissibility can be resolved before CommitGate eligibility, CommitGate decision, and final receipt
```

## Short version

NEO Guard is the gate for the person holding the big red override button.

The button may still exist. It is no longer invisible.
