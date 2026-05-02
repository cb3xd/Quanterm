from enum import StrEnum
from pydantic import BaseModel, Field
from typing import Dict, Any, List, TypeAlias

RawOrderbook: TypeAlias = Dict[str, Any]
RawTrade: TypeAlias = Dict[str, Any]
RawTradeList: TypeAlias = List[RawTrade]


class StreamType(StrEnum):
    ORDERBOOK = "watchOrderBook"
    TRADES = "watchTrades"


class TradeSchema(BaseModel):
    event_type: str = Field(alias="e")
    event_time: int = Field(alias="E")
    transaction_time: int = Field(alias="T")
    symbol: str = Field(alias="s")
    trade_id: int = Field(alias="t")
    price: float = Field(alias="p")
    quantity: float = Field(alias="q")
    order_type: str = Field(alias="X")
    is_maker: bool = Field(alias="m")


class TradeWrapper(BaseModel):
    info: TradeSchema


class TradesBatch(BaseModel):
    trades: List[TradeSchema]
    symbol: str


class OrderbookSchema(BaseModel):
    bids: list[list[float]] = Field(alias="bids")
    asks: list[list[float]] = Field(alias="asks")
    symbol: str = Field(alias="symbol")
    timestamp: int = Field(alias="timestamp")
