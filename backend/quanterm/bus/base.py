import asyncio
import logging
from sched import Event
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


class EventRegistry:
    def __init__(self) -> None:
        self.listeners: defaultdict[str, set[EventHandler]] = defaultdict(set)
        self.events: defaultdict[EventHandler, set[str]] = defaultdict(set)

    def register(self, event_id: str, handler: EventHandler):
        self.listeners[event_id].add(handler)
        self.events[handler].add(event_id)

    def get_listeners(self, event_id: str) -> set[EventHandler]:
        return self.listeners.get(event_id, set())

    def get_events(self, handler: EventHandler) -> set[str]:
        return self.events.get(handler, set())

    def remove_listener(self, event_id: str, handler: EventHandler):
        if event_id in self.listeners:
            self.listeners[event_id].discard(handler)
            self.events[handler].discard(event_id)
            if not self.listeners[event_id]:
                del self.listeners[event_id]
            if not self.events[handler]:
                del self.events[handler]

    def unregister_all(self, handler: EventHandler):
        events = self.events.get(handler)
        if events is None:
            return
        for event in events.copy():
            self.remove_listener(event, handler)


class EventBus:
    def __init__(self) -> None:
        self._listeners: defaultdict[str, set[EventHandler]] = defaultdict(set)
        self._handler_events: defaultdict[EventHandler, set[str]] = defaultdict(set)
        self.event_registry = EventRegistry()
        self._background_tasks: set[asyncio.Task] = set()

    def on(
        self, event: str, handler: Optional[EventHandler] = None
    ) -> Callable[[EventHandler], Listener] | Listener:
        def decorator(handler_function: EventHandler) -> Listener:
            self.event_registry.register(event_id=event, handler=handler_function)
            return Listener(self, event, handler_function)

        if handler is None:
            return decorator
        else:
            return decorator(handler)

    async def publish(self, event: str, message: Struct) -> None:
        listeners = self.event_registry.get_listeners(event)
        if not listeners:
            return
        for listener in listeners:
            try:
                await listener(message)
            except Exception:
                pass

    def remove_listener(self, event: str, handler: EventHandler) -> None:
        self.event_registry.remove_listener(event, handler)

    def unregister_all(self, handler: EventHandler):
        self.event_registry.unregister_all(handler)

    def get_listeners(self) -> dict[str, set[EventHandler]]:
        logging.getLogger("uvicorn").info("GET LISTENERS CALLED")
        return self._listeners.copy()


_event_bus_instance = EventBus()


def get_event_bus() -> EventBus:
    return _event_bus_instance
