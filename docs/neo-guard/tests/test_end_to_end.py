from neo_guard import CommitGateRequest, NeoGuardRequest, run_neo_to_commit_flow


def test_neo_guard_blocks_upstream_so_commit_gate_not_called():
    neo_req = NeoGuardRequest(
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
    commit_req = CommitGateRequest(
        action_type="approve_payment",
        consequence_class="high",
        authority_token_valid=True,
        scope_valid=True,
        payload_hash_present=True,
        nonce_fresh=True,
        audit_sink_available=True,
    )

    flow = run_neo_to_commit_flow(neo_req, commit_req)

    assert flow["neo_guard"]["outcome"] == "HOLD"
    assert flow["commit_gate"] is None
    assert flow["final_record"]["final_decision"] == "REFUSE"
    assert flow["final_record"]["final_reason"] == "commit_gate_blocked_by_neo_guard"
    assert flow["final_record"]["downstream_effect"] == "NO_DOWNSTREAM_EXECUTION_ATTEMPT"
    assert flow["final_record"]["final_receipt_hash"]


def test_neo_allows_but_commit_gate_refuses_invalid_authority_token():
    neo_req = NeoGuardRequest(
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
    commit_req = CommitGateRequest(
        action_type="approve_payment",
        consequence_class="high",
        authority_token_valid=False,
        scope_valid=True,
        payload_hash_present=True,
        nonce_fresh=True,
        audit_sink_available=True,
    )

    flow = run_neo_to_commit_flow(neo_req, commit_req)

    assert flow["neo_guard"]["outcome"] == "ALLOW"
    assert flow["chain_record"]["commit_gate_status"] == "COMMIT_GATE_ELIGIBLE"
    assert flow["commit_gate"]["decision"] == "REFUSE"
    assert flow["final_record"]["final_decision"] == "REFUSE"
    assert flow["final_record"]["final_reason"] == "authority_token_invalid"
    assert flow["final_record"]["downstream_effect"] == "COMMIT_REFUSED_NO_EFFECT"


def test_neo_allows_and_commit_gate_executes_when_all_conditions_hold():
    neo_req = NeoGuardRequest(
        operator_id="human-007",
        role="ops_lead",
        authority_scope=["approve_payment"],
        action_type="approve_payment",
        consequence_class="high",
        override_requested=True,
        reason="documented emergency exception with second authority",
        state_signal="stable",
        time_pressure=False,
        repeat_override_count=0,
        recent_refusal_count=0,
        second_authority_present=True,
    )
    commit_req = CommitGateRequest(
        action_type="approve_payment",
        consequence_class="high",
        authority_token_valid=True,
        scope_valid=True,
        payload_hash_present=True,
        nonce_fresh=True,
        audit_sink_available=True,
    )

    flow = run_neo_to_commit_flow(neo_req, commit_req)

    assert flow["neo_guard"]["outcome"] == "ALLOW"
    assert flow["chain_record"]["commit_gate_status"] == "COMMIT_GATE_ELIGIBLE"
    assert flow["commit_gate"]["decision"] == "EXECUTE"
    assert flow["final_record"]["final_decision"] == "EXECUTE"
    assert flow["final_record"]["final_reason"] == "commit_admissible"
    assert flow["final_record"]["downstream_effect"] == "COMMIT_ALLOWED"
    assert flow["final_record"]["final_receipt_hash"]
