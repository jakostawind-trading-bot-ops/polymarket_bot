from dishka import provide, Provider, Scope

from bot.state.trading_state import TradingState

from bot.repositories.abstract.tracking_markets import TrackingMarketsRepoABC
from bot.repositories.memory.tracking_markets import MemTrackingMarketsRepo

class TradingStateProvider(Provider):
    scope = Scope.APP
    
    tracking_markets = provide(MemTrackingMarketsRepo, provides=TrackingMarketsRepoABC)
    
    trading_state = provide(TradingState)