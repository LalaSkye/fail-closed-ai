from neo_guard.chain import build_commit_chain_receipt
from neo_guard.commit_gate import CommitGateRequest, resolve_commit
from neo_guard.models import NeoGuardRequest
from neo_guard.receipts import sha256_receipt


def run_neo_to_commit_flow(
    neo_request: NeoGuardRequest,
    commit_request: CommitGateRequest,
) -> dict:
    """Run NEO Guard before a bounded mock CommitGate.

    If NEO Guard does not allow authority elevation, CommitGate is not called.
    If NEO Guard allows authority elevation, CommitGate evaluates its own commit
    admissibility conditions and emits a receipt.
    """

    chain = build_commit_chain_receipt(neo_request)
    chain_record = chain["chain_record"]

    if not chain_record["commit_gate_may_be_called"]:
        final_decision = "REFUSE"
        final_reason = "commit_gate_blocked_by_neo_guard"
        commit_gate = None
        downstream_effect = "NO_DOWNSTREAM_EXECUTION_ATTEMPT"
    else:
        commit_gate_response = resolve_commit(commit_request)
        commit_gate = commit_gate_response.to_dict()
        final_decision = commit_gate_response.decision.value
        final_reason = commit_gate_response.reason
        downstream_effect = "COMMIT_ALLOWED" if commit_gate_response.commit_allowed else "COMMIT_REFUSED_NO_EFFECT"

    final_record = {
        "flow": "NEO_GUARD_TO_COMMIT_GATE_END_TO_END",
        "neo_guard_receipt_hash": chain["neo_guard"]["receipt_hash"],
        "chain_receipt_hash": chain_record["chain_receipt_hash"],
        "commit_gate_receipt_hash": commit_gate["receipt_hash"] if commit_gate else None,
        "neo_guard_outcome": chain["neo_guard"]["outcome"],
        "commit_gate_status": chain_record["commit_gate_status"],
        "final_decision": final_decision,
        "final_reason": final_reason,
        "downstream_effect": downstream_effect,
    }
    final_receipt_hash = sha256_receipt(final_record)
    final_record["final_receipt_hash"] = final_receipt_hash

    return {
        "neo_guard": chain["neo_guard"],
        "chain_record": chain_record,
        "commit_gate": commit_gate,
        "final_record": final_record,
    }
