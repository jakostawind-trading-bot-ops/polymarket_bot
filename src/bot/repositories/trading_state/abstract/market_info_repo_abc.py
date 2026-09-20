from abc import ABC, abstractmethod

from bot.entities.market_info import MarketInfo

class MarketInfoRepoABC(ABC):
    @abstractmethod
    async def add_market(self, market_info: MarketInfo):
        pass