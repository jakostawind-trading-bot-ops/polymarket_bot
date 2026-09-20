from abc import ABC, abstractmethod

from bot.repositories.trading_state.abstract.market_state_repo_abc import MarketStateRepoABC
from bot.entities.market_info import MarketInfo

class TradingStateRepoABC(ABC):
    market_state_repo: MarketStateRepoABC
    
    @abstractmethod
    async def track_market(self, market_info: MarketInfo):
        pass
    
    @abstractmethod
    async def get_market_state_repo(self, market_id: int):
        pass
    
    @abstractmethod
    async def get_all_data(self):
        pass