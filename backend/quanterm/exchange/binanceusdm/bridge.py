from quanterm.bus.base import get_event_bus
from quanterm.exchange.binanceusdm.utils import get_stream_id
from quanterm.exchange.binanceusdm.ws import BinanceWebsocket
from quanterm.exchange.constants import ExchangeID
from quanterm.schemas import FastApiSubscribePacket


class BinanceFapiWebsocketBridge:
    def __init__(self, ws: BinanceWebsocket) -> None:
        self.ws = ws
        self.event_bus = get_event_bus()
        self.event_bus.on(f"{ExchangeID.binanceusdm}.subscribe", self.handle_sub_packet)

    async def handle_sub_packet(self, packet: FastApiSubscribePacket):
        stream_id = get_stream_id(packet.symbol, packet.stream_type, packet.interval)
        print(stream_id)
        if stream_id is None:
            return
        await self.ws.subscribe(stream_id)
