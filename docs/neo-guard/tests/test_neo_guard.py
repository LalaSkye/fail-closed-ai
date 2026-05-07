from neo_guard.guard import resolve_operator_standing
from neo_guard.models import NeoGuardOutcome, NeoGuardRequest


def test_low_consequence_in_scope_stable_operator_allowed():
    req = NeoGuardRequest(
        operator_id="human-001",
        role="reviewer",
        authority_scope=["send_message"],
        action_type="send_message",
        consequence_class="low",
        override_requested=False,
        reason="routine approved response",
        state_signal="stable",
    )

    res = resolve_operator_standing(req)

    assert res.outcome == NeoGuardOutcome.ALLOW
    assert res.authority_elevation_allowed is True
    assert res.commit_gate_may_be_called is True
    assert res.receipt_hash


def test_out_of_scope_operator_refused():
    req = NeoGuardRequest(
        operator_id="human-002",
        role="support_agent",
        authority_scope=["send_message"],
        action_type="approve_payment",
        consequence_class="high",
        override_requested=False,
        reason="urgent customer issue",
        state_signal="stable",
    )

    res = resolve_operator_standing(req)

    assert res.outcome == NeoGuardOutcome.REFUSE
    assert res.authority_elevation_allowed is False
    assert res.commit_gate_may_be_called is False
    assert res.reason == "operator_authority_scope_invalid"


def test_high_consequence_pressured_override_held_without_second_authority():
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

    res = resolve_operator_standing(req)

    assert res.outcome == NeoGuardOutcome.HOLD
    assert res.authority_elevation_allowed is False
    assert res.commit_gate_may_be_called is False
    assert res.reason == "high_consequence_override_requires_stable_operator_or_second_authority"


def test_high_consequence_pressured_override_allowed_with_second_authority():
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

    res = resolve_operator_standing(req)

    assert res.outcome == NeoGuardOutcome.ALLOW
    assert res.authority_elevation_allowed is True
    assert res.commit_gate_may_be_called is True


def test_override_without_reason_refused():
    req = NeoGuardRequest(
        operator_id="human-005",
        role="admin",
        authority_scope=["*"],
        action_type="release_external_action",
        consequence_class="medium",
        override_requested=True,
        reason="   ",
        state_signal="stable",
    )

    res = resolve_operator_standing(req)

    assert res.outcome == NeoGuardOutcome.REFUSE
    assert res.reason == "override_requires_inspectable_reason"


def test_compromised_operator_state_halts():
    req = NeoGuardRequest(
        operator_id="human-006",
        role="admin",
        authority_scope=["*"],
        action_type="release_external_action",
        consequence_class="critical",
        override_requested=True,
        reason="manual intervention",
        state_signal="compromised",
    )

    res = resolve_operator_standing(req)

    assert res.outcome == NeoGuardOutcome.HALT
    assert res.authority_elevation_allowed is False
    assert res.commit_gate_may_be_called is False
