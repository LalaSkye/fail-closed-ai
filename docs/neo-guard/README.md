# NEO Guard — Human Node Admissibility Layer

**Status:** v0.1 design + runnable proof surface  
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

## Minimal proof surface

This folder contains:

- `neo_guard/guard.py` — deterministic operator-standing resolver
- `neo_guard/models.py` — request / response models
- `neo_guard/receipts.py` — canonical SHA-256 receipt hashing
- `examples/override_attempt_blocked.json` — example blocked override
- `tests/test_neo_guard.py` — expected HOLD / REFUSE / ALLOW behaviours
- `SPEC_v0.1.md` — design specification
- `CLAIM_BOUNDARY_v0.1.md` — public claim limits

## What this does not prove

This does not prove:

- humans are safe
- emotion can be measured clinically
- all bad overrides are prevented
- this is a production deployment
- this replaces CommitGate
- this is a certification claim

It proves only a bounded mechanism:

```text
human override can be intercepted, evaluated, blocked, and receipted before consequence binds
```

## Short version

NEO Guard is the gate for the person holding the big red override button.

The button may still exist. It is no longer invisible.
