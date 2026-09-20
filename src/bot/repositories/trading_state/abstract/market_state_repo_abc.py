from abc import ABC, abstractmethod

from bot.repositories.trading_state.abstract.market_info_repo_abc import MarketInfoRepoABC

class MarketStateRepoABC(ABC):
    market_info_repo: MarketInfoRepoABC