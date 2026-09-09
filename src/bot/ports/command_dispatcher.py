from typing import Protocol

from bot.commands.command import Command

class CommandDispatcher(Protocol):
    async def dispatch(self, command: Command) -> None:
        ...