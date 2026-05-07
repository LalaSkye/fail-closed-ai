from dataclasses import dataclass, asdict
from enum import Enum
from typing import Literal


class NeoGuardOutcome(str, Enum):
    ALLOW = "ALLOW"
    HOLD = "HOLD"
    ESCALATE = "ESCALATE"
    REFUSE = "REFUSE"
    HALT = "HALT"


StateSignal = Literal["stable", "uncertain", "pressured", "overloaded", "compromised"]
ConsequenceClass = Literal["low", "medium", "high", "critical"]


@dataclass(frozen=True)
class NeoGuardRequest:
    operator_id: str
    role: str
    authority_scope: list[str]
    action_type: str
    consequence_class: ConsequenceClass
    override_requested: bool
    reason: str
    state_signal: StateSignal
    time_pressure: bool = False
    repeat_override_count: int = 0
    recent_refusal_count: int = 0
    second_authority_present: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class NeoGuardResponse:
    outcome: NeoGuardOutcome
    operator_standing: str
    authority_elevation_allowed: bool
    commit_gate_may_be_called: bool
    reason: str
    receipt_hash: str
    record: dict

    def to_dict(self) -> dict:
        data = asdict(self)
        data["outcome"] = self.outcome.value
        return data
