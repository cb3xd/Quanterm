import socket
import struct
from quanterm.api.socket_types import ExchangeID
from quanterm.types import KlineIntervals, StreamTypes

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 9999))
server.listen(5)

stream_type_map: list[str | None] = [None] * 256
interval_map: list[str | None] = [None] * 256
exchange_map: list[str | None] = [None] * 256


for index, member in enumerate(ExchangeID):
    exchange_map[index] = member.value
for index, member in enumerate(StreamTypes):
    stream_type_map[index] = member.value
for index, member in enumerate(KlineIntervals):
    interval_map[index] = member.value


def pretty_print_hex(data: bytes):
    print(data.hex(" ").upper())


def unpack_msg(data: bytes):
    if struct.unpack(">H", data[0:2])[0] != 47802:
        return
    header = data[0:6]
    payload_length = int.from_bytes(header[2:4])
    payload = data[6 : 6 + payload_length]
    pretty_print_hex(payload)


def parse_sub_message(header, payload):
    num_streams = payload[0]
    streams = []
    offset = 1

    for i in range(num_streams):
        stream = parse_stream(payload, offset)
        streams.append(stream)
        offset += 35

    print(streams)


def parse_stream(payload: bytes, offset: int):
    exchange_byte = payload[offset]
    symbol_bytes = payload[offset + 1 : offset + 33]
    stream_type_byte = payload[offset + 33]

    print(exchange_byte, symbol_bytes, stream_type_byte)
    return {
        "exchange": exchange_map[exchange_byte],
        "symbol": symbol_bytes.decode().strip("\x00"),
        "stream_type": stream_type_map[stream_type_byte],
    }


try:
    while True:
        client, address = server.accept()
        msg = client.recv(1024)

        unpack_msg(msg)

        client.send("Nigga wait".encode())
except KeyboardInterrupt:
    pass
