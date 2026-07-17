import websockets
import asyncio
import msgspec
import json

encoder = msgspec.json.Encoder()
decoder = msgspec.json.Decoder()

generated_structs: dict[str, type[msgspec.Struct]] = {}
decoders: dict[str, msgspec.json.Decoder] = {}


async def generate_struct(packet_data: dict, event_type: str):
    fields = []

    for key, value in packet_data.items():
        _ = (key, type(value))
        fields.append(_)

    struct = msgspec.defstruct(event_type, fields)
    generated_structs[event_type] = struct
    print(f"Generated struct at runtime: {generated_structs[event_type]}")
    return struct


async def generate_decoder(struct: type[msgspec.Struct], event_type: str):
    decoder = msgspec.json.Decoder(struct)
    decoders[event_type] = decoder
    return decoder


async def decode_packet(packet: dict):
    packet_data = packet.get("data")

    if packet_data is None:
        return

    event_type = packet_data.get("e")

    struct = generated_structs.get(event_type)

    if struct is None:
        struct = await generate_struct(packet_data, event_type)
        pass

    decoder = decoders.get(event_type)

    if decoder is None:
        decoder = await generate_decoder(struct, event_type)
        pass

    return decoder.decode(encoder.encode(packet_data))


async def main():
    uri = "wss://fstream.binance.com/market/stream"

    async with websockets.connect(uri) as ws:
        payload = json.dumps(
            {"method": "SUBSCRIBE", "params": ["btcusdt@markPrice", "btcusdt@aggTrade"]}
        )
        await ws.send(payload)

        while True:
            try:
                packet = await ws.recv(decode=False)
                decoded_packet = await decode_packet(decoder.decode(packet))
                print(generated_structs.values())

            except websockets.ConnectionClosed:
                print("\nConnection closed")
                break
            except KeyboardInterrupt:
                await ws.close()


if __name__ == "__main__":
    asyncio.run(main())
