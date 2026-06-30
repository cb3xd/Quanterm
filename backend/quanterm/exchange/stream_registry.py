class StreamRegistry:
    def __init__(self) -> None:
        self.event_id_registry = {}
        self.stream_key_registry = {}

    def register(self, event_id: str, stream_key: str):
        self.event_id_registry[event_id] = stream_key
        self.stream_key_registry[stream_key] = event_id

    def unregister(self, event_id: str):
        self.event_id_registry.pop(event_id)

    def get_event_id(self, stream_key: str):
        return self.stream_key_registry.get(stream_key)

    def get_stream_key(self, event_id: str):
        return self.event_id_registry.get(event_id)


_stream_registry = StreamRegistry()


def get_stream_registry():
    return _stream_registry
