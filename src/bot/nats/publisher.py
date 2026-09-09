import json
from dataclasses import asdict
from nats.aio.client import Client

from bot.events.event import Event
from bot.state.general_state import GeneralState

class NatsPublisher():
    def __init__(self,
                 nats_client: Client,
                 general_state: GeneralState):
        self.nats_client = nats_client
        self.general_state = general_state
    
    async def publish(self, event: Event):
        subject = f"bot.{self.general_state.bot_id}.event.{event.event_type}.{event.event_name}"
        
        message = {
                "bot_id": self.general_state.bot_id,
                "bot_status": self.general_state.bot_status,
                "event": {
                    "event_type": event.event_type,
                    "event_name": event.event_name,
                },
                "payload": event.payload,
                "msg": event.msg,
                "timestamp": event.timestamp,
            }
        await self.nats_client.publish(
            subject=subject,
            payload=json.dumps(message).encode("utf-8"),
        )