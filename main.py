import asyncio
from websocket.binance_websocket import StreamType, WebsocketHandler


async def process(out_queue: asyncio.Queue):
    while True:
        event = await out_queue.get()
        print(event)
        out_queue.task_done()


async def main():
    out_queue = asyncio.Queue()
    ws_handler = WebsocketHandler("binanceusdm", out_queue=out_queue)
    pair = "BTC/USDT:USDT"
    stream_type = StreamType.TICKER
    ticker_stream = await ws_handler.subscribe(pair, stream_type)
    asyncio.create_task(process(out_queue))
    await asyncio.sleep(10)
    await ws_handler.unsubscribe(ticker_stream)
    await ws_handler.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutdown signal received. Exiting...")
