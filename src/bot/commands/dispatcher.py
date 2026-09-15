import logging

from bot.commands.command import Command, CommandHandler


logger = logging.getLogger(__name__)


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

        logger.debug(
            "Dispatching command command=%s handler=%s trace_id=%s",
            type(command).__name__,
            type(handler).__name__,
            command.trace_id,
        )

        await handler.handle(command)

        logger.debug(
            "Command dispatch completed command=%s trace_id=%s",
            type(command).__name__,
            command.trace_id,
        )
