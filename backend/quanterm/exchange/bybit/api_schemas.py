from msgspec import Struct, field
import msgspec


class LeverageFilter(msgspec.Struct, rename="camel"):
    min_leverage: str
    max_leverage: str
    leverage_step: str


class PriceFilter(msgspec.Struct, rename="camel"):
    min_price: str
    max_price: str
    tick_size: str


class LotSizeFilter(msgspec.Struct, rename="camel"):
    max_order_qty: str
    min_order_qty: str
    qty_step: str
    post_only_max_order_qty: str | None = None
    max_mkt_order_qty: str | None = None
    min_notional_value: str | None = None


class RiskParameters(msgspec.Struct, rename="camel"):
    price_limit_ratio_x: str
    price_limit_ratio_y: str


class PreListingPhase(msgspec.Struct, rename="camel"):
    phase: str
    start_time: str
    end_time: str | None = None


class AuctionFeeInfo(msgspec.Struct, rename="camel"):
    auction_fee_rate: str
    taker_fee_rate: str
    maker_fee_rate: str


class PreListingInfo(msgspec.Struct, rename="camel"):
    cur_auction_phase: str
    phases: list[PreListingPhase]
    auction_fee_info: AuctionFeeInfo
    skip_call_auction: bool | None = None


class Ticker(msgspec.Struct, rename="camel"):
    symbol: str
    contract_type: str
    status: str
    base_coin: str
    quote_coin: str
    launch_time: str
    delivery_time: str
    price_scale: str
    leverage_filter: LeverageFilter
    price_filter: PriceFilter
    lot_size_filter: LotSizeFilter
    unified_margin_trade: bool
    funding_interval: int
    settle_coin: str
    copy_trading: str
    upper_funding_rate: str
    lower_funding_rate: str
    is_pre_listing: bool
    symbol_id: int | None = None
    delivery_fee_rate: str | None = None
    symbol_type: str | None = None
    display_name: str | None = None
    full_name: str | None = None
    market_region: str | None = None
    underlying_ticker: str | None = None
    forbid_upl_withdrawal: bool | None = None
    risk_parameters: RiskParameters | None = None
    pre_listing_info: PreListingInfo | None = None


class TickerDataPage(msgspec.Struct, rename="camel"):
    category: str
    symbols: list[Ticker] = field(name="list")
    next_page_cursor: str | None = None


class TickerData(msgspec.Struct, rename="camel"):
    ret_code: int
    ret_msg: str
    current_page: TickerDataPage = field(name="result")
    ret_ext_info: dict
    time: int


class Candle(Struct, rename="camel"):
    start_time: str
    open_price: str
    high_price: str
    low_price: str
    close_price: str
    volume: str
    turnover: str


class KlineData(Struct, rename="camel"):
    category: str
    symbol: str
    candles: list[Candle] = field(name="list")
