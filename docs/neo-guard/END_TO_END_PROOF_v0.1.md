# NEO Guard End-to-End Proof v0.1

## Purpose

This proof surface links three stages:

```text
NEO Guard
→ CommitGate eligibility
→ bounded mock CommitGate decision
→ final receipt
```

It demonstrates that human-node admissibility can be checked before the execution boundary is reached.

## Proof paths

### 1. NEO Guard blocks upstream

```text
human override attempt
→ NEO Guard outcome: HOLD
→ CommitGate status: COMMIT_GATE_NOT_CALLED
→ final decision: REFUSE
→ downstream effect: NO_DOWNSTREAM_EXECUTION_ATTEMPT
```

### 2. NEO Guard allows; CommitGate refuses

```text
human override attempt
→ NEO Guard outcome: ALLOW
→ CommitGate status: COMMIT_GATE_ELIGIBLE
→ CommitGate decision: REFUSE
→ downstream effect: COMMIT_REFUSED_NO_EFFECT
```

### 3. NEO Guard allows; CommitGate executes

```text
human override attempt
→ NEO Guard outcome: ALLOW
→ CommitGate status: COMMIT_GATE_ELIGIBLE
→ CommitGate decision: EXECUTE
→ downstream effect: COMMIT_ALLOWED
```

## Receipt chain

The final record includes:

- `neo_guard_receipt_hash`
- `chain_receipt_hash`
- `commit_gate_receipt_hash` where CommitGate is called
- `final_receipt_hash`
- `final_decision`
- `final_reason`
- `downstream_effect`

## What this proves

It proves a bounded end-to-end control path:

```text
operator standing failure blocks CommitGate upstream
operator standing success allows CommitGate evaluation
CommitGate can still refuse independently
final outcome is receipted
```

## What this does not prove

This does not prove:

- production enforcement
- external audit
- integration with live infrastructure
- compliance certification
- all human override risks are prevented

It is a v0.1 runnable proof surface.

## Run

From `docs/neo-guard/`:

```bash
python run_end_to_end_demo.py
pytest
```

## Claim boundary

Use:

```text
NEO Guard now has a v0.1 end-to-end proof path showing human-node admissibility before CommitGate eligibility, CommitGate decision, and final receipt.
```

Do not use:

```text
NEO Guard is production-ready.
NEO Guard certifies human override safety.
NEO Guard guarantees compliance.
```
