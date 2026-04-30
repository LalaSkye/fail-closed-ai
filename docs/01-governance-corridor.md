# Governance Corridor

The governance corridor describes the path from proposed action to real consequence.

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

Each layer removes invalid paths.

A system is not governed because it can describe the corridor.

It is governed only where the corridor binds execution.

---

## Layers

### Proposal

An action is suggested, inferred, requested, or generated.

At this stage, nothing has authority to become consequence.

### Interpretation admissibility

The system checks whether the proposed meaning is valid enough to continue.

Ambiguity is held, not executed.

### Authority check

The system checks whether the actor, source, policy, or human authority can authorise the transition.

### DecisionRecord

The system records the exact authority, scope, expiry, nonce, and target mutation.

### Commit gate

The system verifies the `DecisionRecord` at the moment of commit.

### Execution boundary

The action either becomes consequence or is stopped.

### Receipt

The system records what happened, including refusals.

---

## Rule

The corridor must be evaluated at execution time.

Upstream confidence does not carry authority across the boundary.
