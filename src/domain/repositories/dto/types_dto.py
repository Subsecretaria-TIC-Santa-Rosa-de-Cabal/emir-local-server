from dataclasses import fields
from typing import Any, TypeVar, Dict
T = TypeVar("T", bound="ToDictMixin")

class ToDictMixin:
    _NOT_SENT = object()

    def to_dict(self: T) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for f in fields(self):
            value = getattr(self, f.name)
            if value is not self._NOT_SENT:
                result[f.name] = value
        return result
