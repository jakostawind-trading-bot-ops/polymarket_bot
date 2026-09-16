from dataclasses import dataclass

from bot.events.event import Event

@dataclass
class CommandFailedEvent(Event):
    command_name: str
    error: str