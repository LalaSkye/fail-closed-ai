# NEO Guard v0.1 Specification

## Class

Human-node admissibility layer.

## Purpose

NEO Guard ensures that human authorization, escalation, release, or override attempts are themselves admissible before they can reach the execution boundary.

It protects against the governance failure where:

```text
AI output is governed
human override is trusted by default
consequence binds without inspectable operator standing
```

## Design principle

```text
Neo is inside the geometry, not above it.
```

The human operator is not treated as a sovereign exception to the control system.

## Runtime position

```text
model_output
  → governance_review
  → NEO Guard
  → CommitGate
  → execution | refusal
```

## Inputs

| Field | Meaning |
|---|---|
| `operator_id` | human-node identifier |
| `role` | declared role of operator |
| `authority_scope` | actions this operator may authorize |
| `action_type` | proposed consequence-bearing action |
| `consequence_class` | low / medium / high / critical |
| `override_requested` | whether operator is overriding prior block/hold/refusal |
| `reason` | inspectable reason for authorization or override |
| `state_signal` | stable / uncertain / pressured / overloaded / compromised |
| `time_pressure` | whether urgency pressure is present |
| `repeat_override_count` | repeated override attempts in relevant window |
| `recent_refusal_count` | recent refusal/hold count for same operator/context |
| `second_authority_present` | whether another authorized human confirms the exception |

## Outcomes

| Outcome | Meaning |
|---|---|
| `ALLOW` | operator standing is admissible; CommitGate may be called |
| `HOLD` | operator standing is unresolved; do not call CommitGate |
| `ESCALATE` | repeated or anomalous override pattern requires review |
| `REFUSE` | authority or reason is invalid; do not call CommitGate |
| `HALT` | operator state is compromised; stop the corridor |

## Core rules

1. If operator state is `compromised`, return `HALT`.
2. If `action_type` is outside `authority_scope`, return `REFUSE`.
3. If an override is requested without an inspectable reason, return `REFUSE`.
4. If high/critical consequence override occurs under pressure without second authority, return `HOLD`.
5. If repeat override pattern is excessive, return `ESCALATE`.
6. If high/critical consequence has uncertain operator standing without second authority, return `HOLD`.
7. Otherwise return `ALLOW`.

## Receipt requirement

Every NEO Guard decision emits a deterministic receipt hash over:

- request
- decision record
- outcome
- reason
- authority elevation flag
- CommitGate eligibility flag

## CommitGate relation

NEO Guard does not execute.
NEO Guard does not commit.
NEO Guard only decides whether the human-node authorization path is admissible enough to call CommitGate.

```text
NEO Guard ALLOW → CommitGate may be called
NEO Guard HOLD/REFUSE/ESCALATE/HALT → CommitGate must not be called
```

## Claim boundary

NEO Guard does not prove operator psychology.
It does not diagnose human state.
It does not certify safety.
It does not replace organizational controls.

It proves a bounded mechanism:

```text
human override can be intercepted, classified, blocked, and receipted before execution authority is elevated
```
