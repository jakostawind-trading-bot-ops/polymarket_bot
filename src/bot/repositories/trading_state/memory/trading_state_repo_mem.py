from bot.repositories.trading_state.abstract.trading_state_repo_abc import TradingStateRepoABC
from bot.repositories.trading_state.abstract.market_state_repo_abc import MarketStateRepoABC
from bot.repositories.trading_state.memory.market_state_repo_mem import MarketStateRepoMem

from bot.state.trading_state import TradingState, MarketState
from bot.entities.market_info import MarketInfo

class TradingStateRepoMem(TradingStateRepoABC):
    def __init__(self, trading_state: TradingState):
        self.trading_state = trading_state
        self.market_state_repos: dict[int, MarketStateRepoABC] = {}
        
    async def track_market(self, market_info: MarketInfo):
        market_id = market_info.market_id
        
        if market_id in self.trading_state.tracking_markets:
            raise ValueError(
                  f"Маркет с market_id {market_id} уже отслеживается"
              )
            
        market_state = MarketState(market_info=market_info)
        
        market_state_repo = MarketStateRepoMem(market_state=market_state)
        
        self.trading_state.tracking_markets[market_id] = market_state
        self.market_state_repos[market_id] = market_state_repo
    
    async def untrack_market(self, market_id: str):
        self.trading_state.tracking_markets.pop(market_id, None)
        self.market_state_repos.pop(market_id, None)
        
    async def get_market_state_repo(self, market_id: int):
        return self.market_state_repos[market_id]
    
    async def get_all_data(self):
        return self.trading_state
    
    async def is_empty(self) -> bool:
        return not self.trading_state.tracking_markets