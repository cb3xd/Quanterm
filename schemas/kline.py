from pydantic import BaseModel, Field, ConfigDict

class KlineTick(BaseModel):
    model_config: ConfigDict = ConfigDict(populate_by_name=True)
    start_time: int = Field(alias='t')
    close_time: int = Field(alias='T')
    symbol: str = Field(alias='s')
    open_price: float = Field(alias='o')
    high_price: float = Field(alias='h')
    low_price: float = Field(alias='l')
    close_price: float = Field(alias='c')
    volume: float = Field(alias='v')
    is_closed: bool = Field(alias='x')