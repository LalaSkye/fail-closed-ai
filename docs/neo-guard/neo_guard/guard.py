from neo_guard.models import NeoGuardOutcome, NeoGuardRequest, NeoGuardResponse
from neo_guard.receipts import sha256_receipt


HIGH_CONSEQUENCE = {"high", "critical"}
UNSTABLE_SIGNALS = {"pressured", "overloaded", "compromised"}


def resolve_operator_standing(req: NeoGuardRequest) -> NeoGuardResponse:
    """Resolve whether a human operator may elevate authority before CommitGate.

    NEO Guard does not execute downstream actions. It only determines whether
    the human-node override/authorization path is admissible enough to call the
    execution boundary.
    """

    action_in_scope = req.action_type in req.authority_scope or "*" in req.authority_scope
    reason_present = bool(req.reason and req.reason.strip())
    high_consequence = req.consequence_class in HIGH_CONSEQUENCE
    unstable_state = req.state_signal in UNSTABLE_SIGNALS
    pressure_cluster = (
        req.time_pressure
        or req.repeat_override_count >= 2
        or req.recent_refusal_count >= 2
        or unstable_state
    )

    if req.state_signal == "compromised":
        outcome = NeoGuardOutcome.HALT
        reason = "operator_state_compromised"
    elif not action_in_scope:
        outcome = NeoGuardOutcome.REFUSE
        reason = "operator_authority_scope_invalid"
    elif req.override_requested and not reason_present:
        outcome = NeoGuardOutcome.REFUSE
        reason = "override_requires_inspectable_reason"
    elif req.override_requested and high_consequence and pressure_cluster and not req.second_authority_present:
        outcome = NeoGuardOutcome.HOLD
        reason = "high_consequence_override_requires_stable_operator_or_second_authority"
    elif req.override_requested and req.repeat_override_count >= 3:
        outcome = NeoGuardOutcome.ESCALATE
        reason = "repeat_override_pattern_requires_review"
    elif high_consequence and req.state_signal == "uncertain" and not req.second_authority_present:
        outcome = NeoGuardOutcome.HOLD
        reason = "uncertain_operator_standing_for_high_consequence_action"
    else:
        outcome = NeoGuardOutcome.ALLOW
        reason = "operator_standing_admissible"

    authority_elevation_allowed = outcome == NeoGuardOutcome.ALLOW
    commit_gate_may_be_called = authority_elevation_allowed
    operator_standing = "ADMISSIBLE" if authority_elevation_allowed else outcome.value

    record = {
        "layer": "NEO_GUARD",
        "operator_id": req.operator_id,
        "role": req.role,
        "action_type": req.action_type,
        "consequence_class": req.consequence_class,
        "override_requested": req.override_requested,
        "state_signal": req.state_signal,
        "time_pressure": req.time_pressure,
        "repeat_override_count": req.repeat_override_count,
        "recent_refusal_count": req.recent_refusal_count,
        "second_authority_present": req.second_authority_present,
        "outcome": outcome.value,
        "operator_standing": operator_standing,
        "authority_elevation_allowed": authority_elevation_allowed,
        "commit_gate_may_be_called": commit_gate_may_be_called,
        "reason": reason,
    }
    receipt_hash = sha256_receipt({"request": req.to_dict(), "record": record})
    record["receipt_hash"] = receipt_hash

    return NeoGuardResponse(
        outcome=outcome,
        operator_standing=operator_standing,
        authority_elevation_allowed=authority_elevation_allowed,
        commit_gate_may_be_called=commit_gate_may_be_called,
        reason=reason,
        receipt_hash=receipt_hash,
        record=record,
    )
