# Verdicts

Fail-closed AI uses small, explicit verdicts.

| Verdict | Meaning | Execution |
|---|---|---|
| `ALLOW` | Required proof is valid. | May proceed. |
| `HOLD` | Required proof cannot be validated. | Stops. |
| `DENY` | Transition is invalid or prohibited. | Stops. |

---

## ALLOW

`ALLOW` means the transition has passed the required checks at the boundary where consequence would occur.

It does not mean the system is globally safe.

It means this exact transition is authorised under this exact proof.

---

## HOLD

`HOLD` means the system cannot validate the transition.

Common causes:

- missing authority
- ambiguous scope
- stale proof
- missing receipt path
- uncertain target mutation
- unresolved policy conflict

`HOLD` is not a soft yes.

It stops execution.

---

## DENY

`DENY` means the transition is known to be invalid or prohibited.

Common causes:

- explicit policy prohibition
- replayed nonce
- invalid signature
- out-of-scope action
- blocked actor
- prohibited target

`DENY` stops execution.

---

## Default

When the system cannot decide safely, it returns `HOLD`.

Ambiguity is not permission.
