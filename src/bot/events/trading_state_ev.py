from dataclasses import dataclass

from bot.events.event import Event
from bot.entities.market_info import MarketInfo

@dataclass
class TrackingMarketAddedEvent(Event):
    market_info: MarketInfo