import logging
from dataclasses import dataclass

from bot.commands.command import Command, CommandHandler

@dataclass
class AddTrackingMarketCommand(Command):
    market_id: int
    
class AddTrackingMarketHandle(CommandHandler):
    async def handle(self, command: AddTrackingMarketCommand):
        pass