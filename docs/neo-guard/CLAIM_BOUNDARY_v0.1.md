# NEO Guard Claim Boundary v0.1

## Allowed claim

NEO Guard is a bounded proof surface showing that a human override or authorization path can be intercepted before CommitGate, evaluated for operator standing, blocked when inadmissible, and recorded with a deterministic receipt hash.

## Do not claim

Do not claim that NEO Guard:

- makes humans safe
- detects emotion clinically
- proves intent
- prevents all unsafe overrides
- replaces human review
- replaces CommitGate
- is production-ready
- is certified
- has been externally audited
- guarantees compliance

## Public-safe wording

Use:

```text
NEO Guard makes human override inspectable before consequence binds.
```

Or:

```text
NEO Guard prevents the human node from silently becoming an ungoverned execution bypass.
```

Avoid:

```text
NEO Guard knows when humans are safe.
NEO Guard stops all bad decisions.
NEO Guard solves human-in-the-loop governance.
```

## Evidence boundary

Current evidence is limited to:

- deterministic resolver
- request / response schema
- receipt hash generation
- test vectors
- blocked override example
- written specification

This is a v0.1 design + runnable proof surface, not a deployment claim.
