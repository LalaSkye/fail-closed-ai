from dataclasses import dataclass, asdict
from enum import Enum
from typing import Literal

from neo_guard.receipts import sha256_receipt


class CommitDecision(str, Enum):
    EXECUTE = "EXECUTE"
    REFUSE = "REFUSE"


ConsequenceClass = Literal["low", "medium", "high", "critical"]


@dataclass(frozen=True)
class CommitGateRequest:
    action_type: str
    consequence_class: ConsequenceClass
    authority_token_valid: bool
    scope_valid: bool
    payload_hash_present: bool
    nonce_fresh: bool
    audit_sink_available: bool

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class CommitGateResponse:
    decision: CommitDecision
    commit_allowed: bool
    reason: str
    receipt_hash: str
    record: dict

    def to_dict(self) -> dict:
        data = asdict(self)
        data["decision"] = self.decision.value
        return data


def resolve_commit(req: CommitGateRequest) -> CommitGateResponse:
    """Bounded mock CommitGate for NEO Guard integration proof.

    This is intentionally small. It proves the interface and receipt chain, not
    production enforcement.
    """

    if not req.authority_token_valid:
        decision = CommitDecision.REFUSE
        reason = "authority_token_invalid"
    elif not req.scope_valid:
        decision = CommitDecision.REFUSE
        reason = "scope_invalid"
    elif not req.payload_hash_present:
        decision = CommitDecision.REFUSE
        reason = "payload_hash_missing"
    elif not req.nonce_fresh:
        decision = CommitDecision.REFUSE
        reason = "nonce_not_fresh"
    elif not req.audit_sink_available:
        decision = CommitDecision.REFUSE
        reason = "audit_sink_unavailable"
    else:
        decision = CommitDecision.EXECUTE
        reason = "commit_admissible"

    commit_allowed = decision == CommitDecision.EXECUTE

    record = {
        "layer": "MOCK_COMMIT_GATE",
        "action_type": req.action_type,
        "consequence_class": req.consequence_class,
        "authority_token_valid": req.authority_token_valid,
        "scope_valid": req.scope_valid,
        "payload_hash_present": req.payload_hash_present,
        "nonce_fresh": req.nonce_fresh,
        "audit_sink_available": req.audit_sink_available,
        "decision": decision.value,
        "commit_allowed": commit_allowed,
        "reason": reason,
    }
    receipt_hash = sha256_receipt({"request": req.to_dict(), "record": record})
    record["receipt_hash"] = receipt_hash

    return CommitGateResponse(
        decision=decision,
        commit_allowed=commit_allowed,
        reason=reason,
        receipt_hash=receipt_hash,
        record=record,
    )
