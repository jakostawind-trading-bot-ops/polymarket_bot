from dataclasses import dataclass

from bot.events.event import Event
from bot.entities.market import Market

@dataclass
class MarketAddedInTrackingMarketsEvent(Event):
    market: Market