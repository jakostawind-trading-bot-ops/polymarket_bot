from typing import Protocol

from bot.events.event import Event

class EventPublisher(Protocol):
    async def publish(self, event: Event):
        ...