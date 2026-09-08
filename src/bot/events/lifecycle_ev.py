from dataclasses import dataclass

from bot.events.event import Event

@dataclass
class BotStartedEvent(Event):
    event_type = "lifecycle"
    event_name = "BotStartedEvent"