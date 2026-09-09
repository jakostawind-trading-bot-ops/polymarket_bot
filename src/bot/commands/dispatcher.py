from bot.commands.command import Command, CommandHandler

class CommandDispatcher:
    def __init__(
        self,
        handlers: dict[type[Command], CommandHandler],
    ) -> None:
        self._handlers = handlers

    async def dispatch(self, command: Command) -> None:
        handler = self._handlers.get(type(command))

        if handler is None:
            raise RuntimeError(type(command))

        await handler.handle(command)