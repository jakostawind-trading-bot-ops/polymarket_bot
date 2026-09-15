import logging
from dataclasses import dataclass

from bot.commands.command import Command, CommandHandler


logger = logging.getLogger(__name__)


@dataclass
class RunBotCommand(Command):
    ...


class RunBotHandler(CommandHandler):
    async def handle(
        self,
        command: RunBotCommand,
    ) -> None:
        logger.info(
            "Handling run bot command trace_id=%s",
            command.trace_id,
        )
