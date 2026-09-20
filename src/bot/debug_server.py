import logging
from dataclasses import asdict

from aiohttp import web

from bot.repositories.trading_state.abstract.trading_state_repo_abc import TradingStateRepoABC

logger = logging.getLogger(__name__)

class DebugServer():
    def __init__(self, trading_state_repo: TradingStateRepoABC):
        self.trading_state_repo = trading_state_repo
        app = web.Application()
        app.router.add_get("/trading-state", self.get_trading_state)
        self.runner = web.AppRunner(app, handle_signals=False)
        
    async def start(self):
        await self.runner.setup()
        site = web.TCPSite(
            self.runner,
            host = "127.0.0.1",
            port = 12121,
        )
        await site.start()
        logger.info("Debug HTTP: http://127.0.0.1:12121/")
        
    async def close(self):
        await self.runner.cleanup()
        
    async def get_trading_state(self, request: web.Request): # http://127.0.0.1:12121/trading-state
        data = await self.trading_state_repo.get_all_data()
        return web.json_response(asdict(data))