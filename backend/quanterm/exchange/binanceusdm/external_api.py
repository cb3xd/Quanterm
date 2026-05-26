from decimal import Decimal

import aiohttp
import msgspec

from quanterm.types import KlineIntervals


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


class Candle(msgspec.Struct, array_like=True):
    open_time: int
    open_price: Decimal
    high_price: Decimal
    low_price: Decimal
    close_price: Decimal
    volume: Decimal
    close_time: int
    quote_asset_volume: Decimal
    number_of_trades: int
    taker_buy_base_asset_volume: Decimal
    taker_buy_quote_asset_volume: Decimal


class KlineDataset(msgspec.Struct):
    symbol: str
    interval: KlineIntervals
    candles: list[Candle]


url = "https://fapi.binance.com/fapi/v1"


async def fetch_symbols() -> set[str]:
    exchange_info = await fetch_exchange_info()
    symbols = {s.symbol.lower() for s in exchange_info.symbols}
    return symbols


async def fetch_exchange_info():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{url}/exchangeInfo") as r:
            r.raise_for_status()
            raw_bytes = await r.read()
            data = msgspec.json.decode(raw_bytes, type=ExchangeInfo)
            return data


candle_decoder = msgspec.json.Decoder(list[Candle])
kline_dataset_decoder = msgspec.json.Decoder(KlineDataset)


async def fetch_kline(symbol: str, interval: KlineIntervals):
    params = {"symbol": symbol.upper(), "interval": interval}

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{url}/klines", params=params) as r:
            r.raise_for_status()
            raw_bytes = await r.read()
            candles = candle_decoder.decode(raw_bytes)
            kline = msgspec.convert(
                {"symbol": symbol, "interval": interval, "candles": candles},
                KlineDataset,
            )
            return kline
