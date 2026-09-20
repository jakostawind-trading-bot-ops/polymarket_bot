from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide

from bot.bootstrap import BootstrapSettings
from bot.debug_server import DebugServer
from bot.repositories.trading_state.abstract.trading_state_repo_abc import TradingStateRepoABC

class DebugProvider(Provider):
    scope = Scope.APP

    @provide
    async def provide_debug_server(
        self,
        bootstrap_settings: BootstrapSettings,
        trading_state_repo: TradingStateRepoABC
    ) -> AsyncIterator[DebugServer | None]:
        if not bootstrap_settings.debug:
            yield None
            return

        server = DebugServer(trading_state_repo=trading_state_repo)
        try:
            await server.start()
            yield server
        finally:
            await server.close()