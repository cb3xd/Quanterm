from quanterm.bus.base import get_event_bus
from quanterm.schemas import FastApiSubscribePacket

event_bus = get_event_bus()


async def handle_sub_packet(packet: FastApiSubscribePacket):
    print(packet)


event_bus.on("binanceusdm.subscribe", handle_sub_packet)
