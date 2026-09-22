from dataclasses import dataclass

from bot.events.event import Event

@dataclass
class BotStartedEvent(Event):
    pass
    
@dataclass
class BotRunnedEvent(Event):
    previous_status: str
    current_status: str