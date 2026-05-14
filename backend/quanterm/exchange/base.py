from abc import ABC, abstractmethod
from quanterm.websocket.base import BaseWS


class Exchange(ABC):
    def __init__(self) -> None:
        self.websocket: BaseWS | None

    @abstractmethod
    async def get_symbols(self) -> set[str]: ...

    @abstractmethod
    def get_stream_id(self, symbol: str, stream_type: str) -> str: ...

    @abstractmethod
    async def ws_instance(self) -> BaseWS: ...
