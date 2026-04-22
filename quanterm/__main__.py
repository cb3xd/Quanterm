import asyncio
from quanterm.data.events import StreamType
from quanterm.websocket_handlers.websocket_handler import WebsocketHandler
from quanterm.data.data_normalizer import DataNormalizer

async def main():
    normalizer = DataNormalizer()
    ob_outqueue = normalizer.orderbook_stream_queue
    trades_outqueue = normalizer.trades_stream_queue
    ws_handler = WebsocketHandler(exchange_id="binanceusdm")
    pair = "BTC/USDT:USDT"
    orderbook_stream= await ws_handler.subscribe(pair, stream_type=StreamType.ORDERBOOK, out_queue=ob_outqueue)
    trades_stream = await ws_handler.subscribe(pair, stream_type=StreamType.TRADES, out_queue=trades_outqueue)
    asyncio.create_task(coro=normalizer.process_orderbook())
    asyncio.create_task(coro=normalizer.process_trades())
    await asyncio.sleep(1200)
    await ws_handler.unsubscribe(stream_id=orderbook_stream)
    await ws_handler.unsubscribe(stream_id=trades_stream)
    await ws_handler.close()


if __name__ == "__main__":
    asyncio.run(main())
