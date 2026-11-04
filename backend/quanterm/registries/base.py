from threading import RLock
from typing import Any, Callable, TypeVar, cast, overload

KeyT = TypeVar("KeyT", bound=str)
ValueT = TypeVar("ValueT")


class Registry[KeyT: str, ValueT]:
    def __init__(self) -> None:
        self._entries: dict[KeyT, ValueT] = {}
        self._lock = RLock()

    def _store(self, key: KeyT, obj: Any, force: bool) -> None:
        with self._lock:
            if key in self._entries and not force:
                raise ValueError(f"'{key}' already registered")
            self._entries[key] = cast(ValueT, obj() if isinstance(obj, type) else obj)

    @overload
    def register(self, key: KeyT, value: ValueT, *, force: bool = False) -> None: ...

    @overload
    def register[T](
        self, key: KeyT, value: None = None, *, force: bool = False
    ) -> Callable[[T], T]: ...

    def register(
        self, key: KeyT, value: ValueT | None = None, force: bool = False
    ) -> Callable[[Any], Any] | None:

        if value is not None:
            self._store(key, value, force)
            return None

        def decorator(obj: Any) -> Any:
            self._store(key, obj, force)
            return obj

        return decorator

    def unregister(self, key: KeyT) -> None:
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
