import quanterm.exchange as exchange
from quanterm.exchange.constants import ExchangeID
from quanterm.exchange.exchange_manager import manager
import asyncio

print(exchange)


async def main():
    binanceusdm = manager.get_exchange(ExchangeID.binanceusdm)
    await manager.connect_all_websockets()
    ws = binanceusdm.ws
    ws.subscribe("btcusdt@tradeStream")


if __name__ == "__main__":
    asyncio.run(main())
