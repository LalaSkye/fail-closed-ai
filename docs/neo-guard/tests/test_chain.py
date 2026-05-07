from neo_guard import NeoGuardRequest, build_commit_chain_receipt


def test_blocked_operator_standing_prevents_commit_gate_call():
    req = NeoGuardRequest(
        operator_id="human-003",
        role="ops_lead",
        authority_scope=["approve_payment"],
        action_type="approve_payment",
        consequence_class="high",
        override_requested=True,
        reason="customer escalation",
        state_signal="pressured",
        time_pressure=True,
        repeat_override_count=1,
        recent_refusal_count=2,
        second_authority_present=False,
    )

    chain = build_commit_chain_receipt(req)
    record = chain["chain_record"]

    assert chain["neo_guard"]["outcome"] == "HOLD"
    assert record["commit_gate_status"] == "COMMIT_GATE_NOT_CALLED"
    assert record["commit_gate_may_be_called"] is False
    assert record["downstream_effect"] == "NO_DOWNSTREAM_EXECUTION_ATTEMPT"
    assert record["chain_receipt_hash"]


def test_allowed_operator_standing_makes_commit_gate_eligible():
    req = NeoGuardRequest(
        operator_id="human-004",
        role="ops_lead",
        authority_scope=["approve_payment"],
        action_type="approve_payment",
        consequence_class="high",
        override_requested=True,
        reason="documented emergency exception with second authority",
        state_signal="pressured",
        time_pressure=True,
        repeat_override_count=1,
        recent_refusal_count=2,
        second_authority_present=True,
    )

    chain = build_commit_chain_receipt(req)
    record = chain["chain_record"]

    assert chain["neo_guard"]["outcome"] == "ALLOW"
    assert record["commit_gate_status"] == "COMMIT_GATE_ELIGIBLE"
    assert record["commit_gate_may_be_called"] is True
    assert record["downstream_effect"] == "NO_EFFECT_PRODUCED_BY_NEO_GUARD"
    assert record["chain_receipt_hash"]
