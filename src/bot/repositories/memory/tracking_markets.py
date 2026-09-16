from bot.repositories.abstract.tracking_markets import TrackingMarketsRepo

from bot.entities.market import Market

class MemTrackingMarketsRepo(TrackingMarketsRepo):
    def __init__(self):
        self.tracking_markets: dict[int, Market] = {}
        
    def add(self, market: Market):
        if market.market_id in self.tracking_markets:
            raise ValueError(
                f"Маркет с market_id {market.market_id} уже существует"
            )
        
        self.tracking_markets[market.market_id] = market
        
    def remove(self, market_id):
        if market_id not in self.tracking_markets:
            raise ValueError(
                f"Маркет с market_id {market_id} не найден"
            )
        
        del self.tracking_markets[market_id]