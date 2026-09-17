import logging
from dataclasses import dataclass

from bot.commands.command import Command, CommandHandler
from bot.use_cases.state.trading_state.add_tracking_market_uc import AddTrackingMarketUC

@dataclass
class AddTrackingMarketCommand(Command):
    market_id: int
    
class AddTrackingMarketHandle(CommandHandler):
    def __init__(self, add_tracking_market_uc: AddTrackingMarketUC):
        self.add_tracking_market_uc = add_tracking_market_uc
    
    async def handle(self, command: AddTrackingMarketCommand):
        await self.add_tracking_market_uc.execute(
            market_id=command.market_id
        )