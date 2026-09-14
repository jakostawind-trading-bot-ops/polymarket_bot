import json

from collections.abc import Iterable
from dataclasses import dataclass
from pydantic import BaseModel, ValidationError

from bot.commands.command import Command


class CommandDecodeError(ValueError):
    """Полученная команда не соответствует контракту."""


@dataclass(frozen=True, slots=True)
class CommandRoute:
    message_type: str
    command_type: type[Command]
    payload_schema: type[BaseModel] | None = None


class CommandDecoder:
    def __init__(
        self,
        routes: Iterable[CommandRoute],
    ) -> None:
        self._routes: dict[str, CommandRoute] = {}

        for route in routes:
            if route.message_type in self._routes:
                raise RuntimeError(
                    f"Duplicate command route: {route.message_type}"
                )

            self._routes[route.message_type] = route

    def decode(
        self,
        message_type: str,
        raw_message: bytes,
    ) -> Command:
        try:
            message = json.loads(raw_message)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise CommandDecodeError("Invalid JSON") from error

        if not isinstance(message, dict):
            raise CommandDecodeError("Message must be a JSON object")

        route = self._routes.get(message_type)

        if route is None:
            raise CommandDecodeError(
                f"Unsupported command type: {message_type}"
            )

        trace_id = message.get("command", {}).get("trace_id")

        if not isinstance(trace_id, str) or not trace_id:
            raise CommandDecodeError("Missing or invalid trace_id")

        payload = message.get("payload", {})

        if not isinstance(payload, dict):
            raise CommandDecodeError(
                "Payload must be a JSON object"
            )

        if "trace_id" in payload:
            raise CommandDecodeError(
                "Payload must not contain trace_id"
            )

        if route.payload_schema is None:
            if payload:
                raise CommandDecodeError(
                    f"Command {message_type} does not accept payload"
                )

            command_payload = {}
        else:
            try:
                validated_payload = (
                    route.payload_schema.model_validate(payload)
                )
            except ValidationError as error:
                raise CommandDecodeError(
                    f"Invalid payload for command {message_type}"
                ) from error

            command_payload = validated_payload.model_dump()

        try:
            return route.command_type(
                trace_id=trace_id,
                **command_payload,
            )
        except TypeError as error:
            raise RuntimeError(
                f"Payload schema does not match command {message_type}"
            ) from error
