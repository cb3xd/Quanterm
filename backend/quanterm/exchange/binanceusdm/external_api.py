from decimal import Decimal

import aiohttp
import msgspec

from quanterm.types import KlineIntervals


class RateLimit(msgspec.Struct, rename="camel"):
    interval: str
    interval_num: int
    limit: int
    rate_limit_type: str


class Asset(msgspec.Struct, rename="camel"):
    asset: str
    margin_available: bool
    auto_asset_exchange: str | None


class SymbolFilter(msgspec.Struct, rename="camel"):
    filter_type: str
    max_price: str | None = None
    min_price: str | None = None
    tick_size: str | None = None
    max_qty: str | None = None
    min_qty: str | None = None
    step_size: str | None = None
    limit: int | None = None
    notional: str | None = None
    multiplier_up: str | None = None
    multiplier_down: str | None = None
    multiplier_decimal: str | None = None


class Symbol(msgspec.Struct, rename="camel"):
    symbol: str
    pair: str
    contract_type: str
    delivery_date: int
    onboard_date: int
    status: str
    maint_margin_percent: str
    required_margin_percent: str
    base_asset: str
    quote_asset: str
    margin_asset: str
    price_precision: int
    quantity_precision: int
    base_asset_precision: int
    quote_precision: int
    underlying_type: str
    underlying_sub_type: list[str]
    trigger_protect: str
    filters: list[SymbolFilter]
    order_types: list[str]
    time_in_force: list[str]
    liquidation_fee: str
    market_take_bound: str

    settle_plan: int | None = None


class ExchangeInfo(msgspec.Struct, rename="camel"):
    exchange_filters: list[None]
    rate_limits: list[RateLimit]
    server_time: int
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
