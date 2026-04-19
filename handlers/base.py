from typing import Any, Protocol

class DataStreamHandler(Protocol):
    def process(self, raw_data: Any):
        ...
