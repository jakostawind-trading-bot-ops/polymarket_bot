from bot.repositories.trading_state.abstract.market_info_repo_abc import MarketInfoRepoABC
from bot.state.trading_state import MarketState

from bot.entities.market_info import MarketInfo

class MarketInfoRepoMem(MarketInfoRepoABC):
    def __init__(self, market_state: MarketState):
        self.market_state = market_state
    
    async def add_market(self, market_info: MarketInfo):
        self.market_state.market_info = market_info