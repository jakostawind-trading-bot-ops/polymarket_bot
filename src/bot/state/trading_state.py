from dataclasses import dataclass, field

from bot.entities.market_info import MarketInfo

@dataclass
class TradingState():
    tracking_markets: dict[int, MarketState] = field(default_factory=dict)
    

@dataclass
class MarketState():
    market_info: MarketInfo