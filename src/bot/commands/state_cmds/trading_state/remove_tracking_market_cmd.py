from dataclasses import dataclass

from bot.commands.command import Command, CommandHandler
from bot.use_cases import RemoveTrackingMarketUC

@dataclass
class RemoveTrackingMarketCommand(Command):
    market_id: int
    
class RemoveTrackingMarketHandler(CommandHandler):
    def __init__(self, remove_tracking_market_uc: RemoveTrackingMarketUC):
        self.remove_tracking_market_uc = remove_tracking_market_uc
        
    async def handle(self, command: RemoveTrackingMarketCommand):
        await self.remove_tracking_market_uc.execute(
            market_id=command.market_id
        )