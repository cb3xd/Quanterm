import asyncio
import json
import websockets
import msgspec

encoder = msgspec.json.Encoder()


async def stream_data():
    uri = "ws://localhost:8000/ws/cex"
    async with websockets.connect(uri) as websocket:
        # Prepare payload as bytes
        payload = encoder.encode(
            {
                "method": "sub",
                "events": ["market_price"],
                "exchange": "binanceusdm",
            }
        )
        print(payload)

        await websocket.send(payload)

        while True:
            try:
                response = await websocket.recv()
                print(f"Received: {response}")
            except websockets.ConnectionClosed:
                break


if __name__ == "__main__":
    asyncio.run(stream_data())
