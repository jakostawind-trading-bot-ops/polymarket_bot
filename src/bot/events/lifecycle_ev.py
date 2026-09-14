from dataclasses import dataclass

from bot.events.event import Event

@dataclass
class BotStartedEvent(Event):
    pass
    
# @dataclass
# class BotRunnedEvent(Event):
#     prev_status: str
#     cur_status: str