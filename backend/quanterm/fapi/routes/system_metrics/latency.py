from quanterm.fapi.main import api_router
from quanterm.exchange.exchange_manager import manager


@api_router.get("/system-metrics/latency")
async def get_latency():
    exchanges = manager.active_exchanges
    for exchange in exchanges.values():
        print(exchange)
