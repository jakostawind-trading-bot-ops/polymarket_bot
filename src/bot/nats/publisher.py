import json
from nats.js.client import JetStreamContext

from bot.events.event import Event
from bot.state.general_state import GeneralState

class NatsPublisher():
    def __init__(
        self,
        jetstream: JetStreamContext,
        stream_name: str,
        general_state: GeneralState
    ) -> None:
        self._jetstream = jetstream
        self._stream_name = stream_name
        self._general_state = general_state
        
    async def publish_event(self, event: Event):
        subject = f"bot.{self._general_state.bot_id}.event.{event.event_type}.{event.event_name}"
        
        message = {
            "bot_id": self._general_state.bot_id,
            "bot_status": self._general_state.bot_status,
            "event": {
                "trace_id": str(event.trace_id),
                "event_type": event.event_type,
                "event_name": event.event_name,
            },
            "payload": event.payload,
            "msg": event.msg,
            "timestamp": event.timestamp,
        }
        await self._jetstream.publish(
            subject=subject,
            payload=json.dumps(message).encode("utf-8"),
            stream=self._stream_name
        )