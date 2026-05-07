# NEO Guard → CommitGate Chain Receipt v0.1

## Purpose

This artefact proves that human-node admissibility is resolved before CommitGate may be called.

It closes the bypass pattern:

```text
AI action refused
human overrides under pressure
CommitGate receives elevated authority anyway
consequence binds
```

NEO Guard prevents that by emitting a chain receipt before CommitGate eligibility.

## Chain states

| NEO Guard result | CommitGate status | Meaning |
|---|---|---|
| `ALLOW` | `COMMIT_GATE_ELIGIBLE` | operator standing is admissible enough for CommitGate to evaluate |
| `HOLD` / `REFUSE` / `ESCALATE` / `HALT` | `COMMIT_GATE_NOT_CALLED` | CommitGate is blocked upstream; no downstream execution attempt is allowed |

## Receipt fields

The chain record includes:

- `chain`
- `neo_guard_receipt_hash`
- `neo_guard_outcome`
- `operator_standing`
- `authority_elevation_allowed`
- `commit_gate_status`
- `commit_gate_may_be_called`
- `downstream_effect`
- `reason`
- `chain_receipt_hash`

## What this proves

It proves a bounded transition:

```text
human override attempt
→ NEO Guard operator-standing resolution
→ CommitGate eligibility decision
→ chain receipt
```

If operator standing fails, the receipt shows that CommitGate was not called.

## What this does not prove

This does not prove:

- CommitGate itself executed
- downstream infrastructure was reached
- production enforcement exists
- all human override risks are prevented
- operator psychology was assessed clinically

It proves only:

```text
the human-node path can be blocked upstream and the non-call to CommitGate can be receipted
```

## Runnable demo

From `docs/neo-guard/`:

```bash
python run_chain_demo.py
```

Expected blocked-path signal:

```text
"commit_gate_status": "COMMIT_GATE_NOT_CALLED"
"downstream_effect": "NO_DOWNSTREAM_EXECUTION_ATTEMPT"
```
