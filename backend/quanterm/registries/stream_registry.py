from quanterm.registries.base import Registry


class StreamRegistry:
    def __init__(self) -> None:
        self.event_id_registry = Registry[str, str]()
        self.stream_key_registry = Registry[str, str]()

    def register(self, event_id: str, stream_key: str):
        self.event_id_registry.register(event_id, stream_key)
        self.stream_key_registry.register(stream_key, event_id)

    def unregister(self, event_id: str):
        self.event_id_registry.unregister(event_id)

    def get_event_id(self, stream_key: str):
        return self.stream_key_registry.get(stream_key)

    def get_stream_key(self, event_id: str):
        return self.event_id_registry.get(event_id)
