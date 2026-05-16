from abc import ABC, abstractmethod
from quanterm.websocket.base import BaseWS


class Exchange(ABC):
    @abstractmethod
    async def get_symbols(self) -> set[str]: ...

    @abstractmethod
    async def ws_instance(self) -> BaseWS: ...
