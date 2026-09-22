import logging
from dataclasses import dataclass

from bot.commands.command import Command, CommandHandler
from bot.use_cases import RunBotUc


logger = logging.getLogger(__name__)


@dataclass
class RunBotCommand(Command):
    ...


class RunBotHandler(CommandHandler):
    def __init__(
        self,
        run_bot_uc: RunBotUc
    ):
        self.run_bot_uc = run_bot_uc
        
    async def handle(
        self,
        command: RunBotCommand,
    ) -> None:
        await self.run_bot_uc.execute()
