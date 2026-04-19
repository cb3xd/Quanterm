import asyncio
from websocket.binance_websocket import WebsocketHandler
from handlers import MiniTickerStreamHandler


async def main():
    manager = WebsocketHandler()
    handler = MiniTickerStreamHandler()
    mini_ticker_id = await manager.create_mini_ticker_socket(callback=handler.process)
    while True:
        symbol = "BTCUSDT"
        ticker = handler.get_ticker(symbol)  # Use the new method
        agg_ticker = handler.get_aggregate_tickers()
        if agg_ticker:
            print(agg_ticker)
        else:
            print(f"Ticker for {symbol} not yet received.")

        await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutdown signal received. Exiting...")
