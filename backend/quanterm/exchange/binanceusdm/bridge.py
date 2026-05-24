from quanterm.exchange.base_bridge import BaseBridge
from quanterm.exchange.binanceusdm.utils import get_stream_id
from quanterm.exchange.constants import ExchangeID
from quanterm.schemas import FastApiSubscribePacket
from quanterm.websocket.base import BaseWS


class BinanceFapiWebsocketBridge(BaseBridge):
    def __init__(self, ws: BaseWS) -> None:
        super().__init__(exchange_id=ExchangeID.binanceusdm, ws=ws)

    def get_stream_id(self, packet: FastApiSubscribePacket) -> str | None:
        return get_stream_id(packet.symbol, packet.stream_type, packet.interval)
