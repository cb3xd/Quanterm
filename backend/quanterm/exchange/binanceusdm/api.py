import aiohttp
import msgspec


class RateLimit(msgspec.Struct):
    interval: str
    intervalNum: int
    limit: int
    rateLimitType: str


class Asset(msgspec.Struct):
    asset: str
    marginAvailable: bool
    autoAssetExchange: str | None


class SymbolFilter(msgspec.Struct):
    filterType: str
    maxPrice: str | None = None
    minPrice: str | None = None
    tickSize: str | None = None
    maxQty: str | None = None
    minQty: str | None = None
    stepSize: str | None = None
    limit: int | None = None
    notional: str | None = None
    multiplierUp: str | None = None
    multiplierDown: str | None = None
    multiplierDecimal: str | None = None


class Symbol(msgspec.Struct):
    symbol: str
    pair: str
    contractType: str
    deliveryDate: int
    onboardDate: int
    status: str
    maintMarginPercent: str
    requiredMarginPercent: str
    baseAsset: str
    quoteAsset: str
    marginAsset: str
    pricePrecision: int
    quantityPrecision: int
    baseAssetPrecision: int
    quotePrecision: int
    underlyingType: str
    underlyingSubType: list[str]
    triggerProtect: str
    filters: list[SymbolFilter]
    orderTypes: list[str]
    timeInForce: list[str]
    liquidationFee: str
    marketTakeBound: str

    settlePlan: int | None = None


class ExchangeInfo(msgspec.Struct):
    exchangeFilters: list[None]
    rateLimits: list[RateLimit]
    serverTime: int
    assets: list[Asset]
    symbols: list[Symbol]
    timezone: str


async def fetch_symbols() -> set[str]:
    exchange_info = await fetch_exchange_info()
    symbols = {s.symbol.lower() for s in exchange_info.symbols}
    return symbols


async def fetch_exchange_info():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://fapi.binance.com/fapi/v1/exchangeInfo") as r:
            r.raise_for_status()
            raw_bytes = await r.read()
            data = msgspec.json.decode(raw_bytes, type=ExchangeInfo)
            return data
