import json

from neo_guard import CommitGateRequest, NeoGuardRequest, run_neo_to_commit_flow


def print_case(title: str, neo_req: NeoGuardRequest, commit_req: CommitGateRequest) -> None:
    print(f"\n=== {title} ===")
    flow = run_neo_to_commit_flow(neo_req, commit_req)
    print(json.dumps(flow["final_record"], indent=2, sort_keys=True))


if __name__ == "__main__":
    blocked_neo = NeoGuardRequest(
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

    allowed_neo = NeoGuardRequest(
        operator_id="human-004",
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

    good_commit = CommitGateRequest(
        action_type="approve_payment",
        consequence_class="high",
        authority_token_valid=True,
        scope_valid=True,
        payload_hash_present=True,
        nonce_fresh=True,
        audit_sink_available=True,
    )

    bad_commit = CommitGateRequest(
        action_type="approve_payment",
        consequence_class="high",
        authority_token_valid=False,
        scope_valid=True,
        payload_hash_present=True,
        nonce_fresh=True,
        audit_sink_available=True,
    )

    print_case("1. NEO Guard blocks before CommitGate", blocked_neo, good_commit)
    print_case("2. NEO Guard allows; CommitGate refuses", allowed_neo, bad_commit)
    print_case("3. NEO Guard allows; CommitGate executes", allowed_neo, good_commit)
