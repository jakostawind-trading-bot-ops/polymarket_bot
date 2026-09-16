from abc import ABC, abstractmethod

from bot.entities.market import Market

class TrackingMarketsRepo(ABC):
    @abstractmethod
    def add(self, market: Market):
        pass
    
    def remove(self, market_id):
        pass