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
        self._listeners: defaultdict[str, set[EventHandler]] = defaultdict(set)
        self._handler_events: defaultdict[EventHandler, set[str]] = defaultdict(set)
        self._background_tasks: set[asyncio.Task] = set()

    def on(
        self, event: str, handler: Optional[EventHandler] = None
    ) -> Callable[[EventHandler], Listener] | Listener:
        def decorator(handler_function: EventHandler) -> Listener:
            self._listeners[event].add(handler_function)
            self._handler_events[handler_function].add(event)
            return Listener(self, event, handler_function)

        if handler is None:
            return decorator
        else:
            return decorator(handler)

    async def publish(self, event: str, message: Struct) -> None:
        listeners = self._listeners.get(event, [])
        if not listeners:
            return
        for listener in listeners:
            try:
                await listener(message)
            except Exception:
                pass

    def remove_listener(self, event: str, handler: EventHandler) -> None:
        if event in self._listeners:
            self._listeners[event].discard(handler)
            self._handler_events[handler].discard(event)
            if not self._listeners[event]:
                del self._listeners[event]
            if not self._handler_events[handler]:
                del self._handler_events[handler]

    def unregister_all(self, handler: EventHandler):
        events = self._handler_events.get(handler)
        if events is None:
            return
        for event in events.copy():
            self.remove_listener(event, handler)

    def get_listeners(self) -> dict[str, set[EventHandler]]:
        return self._listeners.copy()


_event_bus_instance = EventBus()


def get_event_bus() -> EventBus:
    return _event_bus_instance
