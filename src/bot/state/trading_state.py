from dataclasses import dataclass

from bot.repositories.abstract.tracking_markets import TrackingMarketsRepoABC

@dataclass
class TradingState():
    tracking_markets: TrackingMarketsRepoABC