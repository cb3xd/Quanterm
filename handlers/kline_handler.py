from schemas.kline import KlineTick
from typing import Any

class KlineStreamHandler:
    async def process(self, raw_data: Any) -> KlineTick:
        kline_tick = KlineTick.model_validate(raw_data['k'])
        print(f'[{raw_data['s']}]: {kline_tick.close_price}')
        return kline_tick
