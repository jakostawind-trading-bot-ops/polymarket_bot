import logging
from dataclasses import dataclass

from bot.commands.command import Command, CommandHandler

logger = logging.getLogger(__name__)

@dataclass
class AddAccountStateCommand(Command):
    nickname: str
    wallet: str
    
class AddAccountStateHandler(CommandHandler):
    async def handle(self, command: AddAccountStateCommand):
        logger.info(
            "AddAccountStateHandler runned, trace_id=%s",
            command.trace_id
        )