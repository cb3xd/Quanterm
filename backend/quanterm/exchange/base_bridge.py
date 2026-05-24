from abc import ABC, abstractmethod

from quanterm.bus.base import get_event_bus
from quanterm.exchange.constants import ExchangeID
from quanterm.schemas import FastApiSubscribePacket
from quanterm.websocket.base import BaseWS


class BaseBridge(ABC):
    def __init__(self, exchange_id: ExchangeID, ws: BaseWS) -> None:
        self.exchange_id = exchange_id
        self.ws = ws
        self.event_bus = get_event_bus()

        self.event_bus.on(f"{self.exchange_id}.subscribe", self.handle_sub_packet)

    @abstractmethod
    def get_stream_id(self, packet: FastApiSubscribePacket) -> str | None:
        """Every specific bridge must implement its own logic
        to decode a packet to its exchange specific stream ID string."""
        ...

    async def handle_sub_packet(self, packet: FastApiSubscribePacket):
        stream_id = self.get_stream_id(packet)
        if stream_id is None:
            return
        await self.ws.subscribe(stream_id)
