import json
from collections.abc import Iterable
from dataclasses import dataclass
from pydantic import ValidationError

from nats_contracts.control.bot.v1.common import ControlMessage

from bot.commands.command import Command


class CommandDecodeError(ValueError):
    """Полученная команда не соответствует контракту."""


@dataclass(frozen=True, slots=True)
class CommandRoute:
    msg_type: str # суффикс NATS сабджект для поиска команды. Например "lifecycle.RunBotCommand"
    msg_model: type[ControlMessage] # класс модели из nats_contracts
    command_model: type[Command] # внутренняя команда бота


class CommandDecoder:
    def __init__(
        self,
        routes: Iterable[CommandRoute],
    ) -> None:
        self._routes: dict[str, CommandRoute] = {}

        for route in routes:
            if route.msg_type in self._routes:
                raise RuntimeError(
                    f"Duplicate command route: {route.msg_type}"
                )

            self._routes[route.msg_type] = route

    def decode(
        self,
        msg_type: str,
        raw_message: bytes,
    ) -> Command:

        route = self._routes.get(msg_type)

        if route is None:
            raise CommandDecodeError(
                f"Unsupported command type: {msg_type}"
            )

        try:
            message = route.msg_model.model_validate_json(
                raw_message
            )
        except ValidationError as error:
            raise CommandDecodeError(
                f"Invalid mmessage contract: {msg_type}"
            ) from error
            
        try:
            return route.command_model(
                trace_id=message.message.trace_id,
                **message.payload.model_dump(),
            )
        except TypeError as error:
            raise RuntimeError(
                f"Message payload does not match command {msg_type}"
            ) from error