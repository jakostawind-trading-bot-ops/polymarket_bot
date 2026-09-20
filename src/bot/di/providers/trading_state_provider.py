from dishka import Provider, Scope, provide

from bot.state.trading_state import TradingState
from bot.repositories.trading_state.abstract.trading_state_repo_abc import TradingStateRepoABC
from bot.repositories.trading_state.memory.trading_state_repo_mem import TradingStateRepoMem


class TradingStateProvider(Provider):
    scope = Scope.APP

    @provide
    def trading_state(self) -> TradingState:
        return TradingState(tracking_markets={})

    trading_state_repo = provide(
        TradingStateRepoMem,
        provides=TradingStateRepoABC,
    )