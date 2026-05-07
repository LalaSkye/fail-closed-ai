import json

from neo_guard import NeoGuardRequest, build_commit_chain_receipt


if __name__ == "__main__":
    request = NeoGuardRequest(
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

    chain = build_commit_chain_receipt(request)
    print(json.dumps(chain, indent=2, sort_keys=True))
