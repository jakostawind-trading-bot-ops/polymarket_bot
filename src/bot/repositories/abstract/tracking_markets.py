from abc import ABC, abstractmethod

from bot.entities.market import Market

class TrackingMarketsRepoABC(ABC):
    @abstractmethod
    async def add(self, market: Market):
        pass
    
    async def remove(self, market_id):
        pass