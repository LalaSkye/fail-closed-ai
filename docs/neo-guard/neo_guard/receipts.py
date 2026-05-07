import hashlib
import json
from typing import Any


def canonical(obj: Any) -> str:
    if hasattr(obj, "to_dict"):
        obj = obj.to_dict()
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def sha256_receipt(obj: Any) -> str:
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()
