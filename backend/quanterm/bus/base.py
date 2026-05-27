import asyncio
from typing import Optional, TypeAlias, Callable, Any, Coroutine
from collections import defaultdict
from msgspec import Struct

EventHandler: TypeAlias = Callable[[Any], Coroutine[Any, Any, None]]


class Listener:
    def __init__(
        self, event_bus: "EventBus", event: str, handler: EventHandler
    ) -> None:
        self.event_bus = event_bus
        self.event = event
        self.handler = handler

    def unregister(self) -> None:
        self.event_bus.remove_listener(self.event, self.handler)


class EventBus:
    def __init__(self) -> None:
        self._listeners: defaultdict[str, list[EventHandler]] = defaultdict(list)

    def on(
        self, event: str, handler: Optional[EventHandler] = None
    ) -> Callable[[EventHandler], Listener] | Listener:
        def decorator(handler_function: EventHandler) -> Listener:
            self._listeners[event].append(handler_function)
            return Listener(self, event, handler_function)

        if handler is None:
            return decorator
        else:
            return decorator(handler)

    async def publish(self, event: str, message: Struct) -> None:
        listeners = self._listeners.get(event, [])
        if listeners:
            async with asyncio.TaskGroup() as tg:
                for listener in listeners:
                    tg.create_task(self._safe_execute(listener, message))

    def remove_listener(self, event: str, handler: EventHandler) -> None:
        if event in self._listeners:
            self._listeners[event].remove(handler)
            if not self._listeners[event]:
                del self._listeners[event]

    def get_listeners(self, event: str) -> list[EventHandler]:
        return self._listeners[event].copy()

    async def _safe_execute(self, handler: EventHandler, message: Struct) -> None:
        try:
            await handler(message)
        except Exception as e:
            print(f"CRITICAL: Event handler crashed {e}")


_event_bus_instance = EventBus()


def get_event_bus() -> EventBus:
    return _event_bus_instance
