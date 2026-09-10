from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Any
import json

from bot.commands.command import Command


CommandFactory = Callable[[dict[str, Any]], Command]


@dataclass(frozen=True, slots=True)
class CommandRoute:
    message_type: str
    factory: CommandFactory


class CommandDecoder:
    def __init__(self, routes: Iterable[CommandRoute]) -> None:
        self._factories: dict[str, CommandFactory] = {}

        for route in routes:
            if route.message_type in self._factories:
                raise ValueError(
                    f"Duplicate command type: {route.message_type}"
                )

            self._factories[route.message_type] = route.factory

    def decode(self, 
               command_type: str,
               raw_message: bytes) -> Command:
          try:
              message = json.loads(raw_message)
          except (UnicodeDecodeError, json.JSONDecodeError) as error:
              raise RuntimeError("Invalid JSON") from error


          if not isinstance(message, dict):
              raise RuntimeError("Message must be a JSON object")

          factory = self._factories.get(command_type)

          if factory is None:
              raise RuntimeError(
                  f"Unsupported command type: {command_type}"
              )

          return factory(message)