from bot.repositories.trading_state.abstract.market_state_repo_abc import MarketStateRepoABC
from bot.repositories.trading_state.memory.market_info_repo_mem import MarketInfoRepoMem

from bot.state.trading_state import MarketState

class MarketStateRepoMem(MarketStateRepoABC):
    def __init__(self, market_state: MarketState):
        self.market_state = market_state
        self.market_info_repo = MarketInfoRepoMem(market_state=market_state)
        