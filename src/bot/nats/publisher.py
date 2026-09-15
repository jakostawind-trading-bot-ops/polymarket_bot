import logging
from dataclasses import fields

from nats.js.client import JetStreamContext

from nats_contracts.bot.control.v1.common import BotMessage
from nats_contracts.bot.control.v1.common.subjects import generate_bot_to_control_event_subject

from bot.events.event import Event
from bot.state.general_state import GeneralState
from bot.nats.contracts.registry import EVENT_CONTRACTS


logger = logging.getLogger(__name__)


class NatsPublisher():
    def __init__(
        self,
        jetstream: JetStreamContext,
        stream_name: str,
        general_state: GeneralState
    ) -> None:
        self.jetstream = jetstream
        self.stream_name = stream_name
        self.general_state = general_state
    
    @staticmethod
    def build_payload(event: Event):
        excluded = {"message_id", "trace_id", "timestamp"}
        
        return {
            item.name: getattr(event, item.name)
            for item in fields(event)
            if item.name not in excluded
        }
    
    def encode_event(
        self,
        event: Event
    ) -> tuple[str, BotMessage]:
        logger.debug(
            "Encoding event event=%s message_id=%s trace_id=%s",
            type(event).__name__,
            event.message_id,
            event.trace_id,
        )

        contract_type = EVENT_CONTRACTS.get(type(event))
        
        if contract_type is None:
            raise RuntimeError(f"Ивент неподдерживается: {type(event).__name__}")
        
        message = contract_type(
            bot_id=self.general_state.bot_id,
            bot_status=self.general_state.bot_status,
            message={
                "message_id": str(event.message_id),
                "trace_id": str(event.trace_id),
            },
            payload=self.build_payload(event),
            timestamp=event.timestamp
        )
        
        subject = generate_bot_to_control_event_subject(
            bot_id=self.general_state.bot_id,
            event_version=message.message.message_version,
            event_type=message.message.message_type,
            event_name=message.message.message_name
        )

        logger.debug(
            "Event encoded event=%s subject=%s",
            type(event).__name__,
            subject,
        )

        return subject, message
    
    async def publish_event(self, event: Event):
        subject, message = self.encode_event(event)

        logger.info(
            "Publishing event event=%s message_id=%s "
            "trace_id=%s stream=%s subject=%s",
            type(event).__name__,
            event.message_id,
            event.trace_id,
            self.stream_name,
            subject,
        )

        await self.jetstream.publish(
            subject=subject,
            payload=message.model_dump_json().encode("utf-8"),
            stream=self.stream_name
        )

        logger.info(
            "Event published event=%s message_id=%s subject=%s",
            type(event).__name__,
            event.message_id,
            subject,
        )
