from neo_guard.guard import resolve_operator_standing
from neo_guard.models import NeoGuardRequest
from neo_guard.receipts import sha256_receipt


def build_commit_chain_receipt(req: NeoGuardRequest) -> dict:
    """Build a receipt linking NEO Guard standing to CommitGate eligibility.

    This module does not implement CommitGate itself. It proves whether CommitGate
    was allowed to be called after human-node admissibility resolution.
    """

    neo_response = resolve_operator_standing(req)

    if neo_response.commit_gate_may_be_called:
        commit_gate_status = "COMMIT_GATE_ELIGIBLE"
        downstream_effect = "NO_EFFECT_PRODUCED_BY_NEO_GUARD"
        chain_reason = "operator_standing_admissible_commit_gate_may_evaluate"
    else:
        commit_gate_status = "COMMIT_GATE_NOT_CALLED"
        downstream_effect = "NO_DOWNSTREAM_EXECUTION_ATTEMPT"
        chain_reason = "operator_standing_failed_commit_gate_blocked_upstream"

    chain_record = {
        "chain": "NEO_GUARD_TO_COMMIT_GATE",
        "neo_guard_receipt_hash": neo_response.receipt_hash,
        "neo_guard_outcome": neo_response.outcome.value,
        "operator_standing": neo_response.operator_standing,
        "authority_elevation_allowed": neo_response.authority_elevation_allowed,
        "commit_gate_status": commit_gate_status,
        "commit_gate_may_be_called": neo_response.commit_gate_may_be_called,
        "downstream_effect": downstream_effect,
        "reason": chain_reason,
    }

    chain_receipt_hash = sha256_receipt(chain_record)
    chain_record["chain_receipt_hash"] = chain_receipt_hash

    return {
        "neo_guard": neo_response.to_dict(),
        "chain_record": chain_record,
    }
