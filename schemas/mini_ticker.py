from pydantic import BaseModel, Field, ConfigDict
from typing import ClassVar


class MiniTicker(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(populate_by_name=True)

    symbol: str = Field(alias="s")
    open_price: float = Field(alias="o")
    high_price: float = Field(alias="h")
    low_price: float = Field(alias="l")
    close_price: float = Field(alias="c")
    volume: float = Field(alias="v")


class AggregateTickers(BaseModel):
    tickers: dict[str, MiniTicker]
