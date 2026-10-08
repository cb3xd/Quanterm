from threading import RLock
from typing import Generic, TypeVar

KeyT = TypeVar("KeyT", bound=str)
ValueT = TypeVar("ValueT")


class Registry(Generic[KeyT, ValueT]):
    def __init__(self) -> None:
        self._entries: dict[KeyT, ValueT] = {}
        self._lock = RLock()

    def register(self, key: KeyT, value: ValueT = None, force: bool = False):
        def _register(obj):
            with self._lock:
                if key in self._entries and not force:
                    raise ValueError(f"'{key}' already registered")
                if isinstance(obj, type):
                    self._entries[key] = obj()
                else:
                    self._entries[key] = obj
            return obj

        if value is None:
            return _register
        _register(value)
        return None

    def unregister(self, key: KeyT, force: bool = False) -> None:
        with self._lock:
            self._entries.pop(key)

    def get(self, key: KeyT) -> ValueT:
        with self._lock:
            if key not in self._entries:
                raise ValueError(f"'{key}' not found")
            return self._entries[key]

    def setdefault(self, key: KeyT, value: ValueT) -> ValueT:
        with self._lock:
            if key in self._entries:
                return self._entries[key]
            if isinstance(value, type):
                self._entries[key] = value()
            else:
                self._entries[key] = value
            return self._entries[key]

    def list(self) -> dict[KeyT, ValueT]:
        return dict(self._entries)
