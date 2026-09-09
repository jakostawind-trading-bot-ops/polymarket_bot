from typing import Protocol
from bot.commands.command import Command

class CommandSubscriber(Protocol):
    async def start(self) -> None:
        ...

    async def close(self) -> None:
        ...