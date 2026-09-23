import asyncio
import json
from unittest.mock import AsyncMock
from uuid import UUID

import pytest
from nats.js.client import JetStreamContext
from nats_contracts.bot.control.v1.failed import CommandFailedEvMsg
from nats_contracts.bot.control.v1.lifecycle import BotStartedEvMsg

from bot.events.event import Event
from bot.events.failed_ev import CommandFailedEvent
from bot.events.lifecycle_ev import BotStartedEvent
from bot.lifecycle.statuses import LifecycleStatus
from bot.transport.nats.publisher import NatsPublisher
from bot.state.general_state import GeneralState


@pytest.fixture
def publisher():
    return NatsPublisher(
        AsyncMock(spec=JetStreamContext),
        "BOT_EVENTS",
        GeneralState("ABCDEFGHJKMNPQRS", LifecycleStatus.STARTED),
    )


@pytest.fixture
def started_event():
    return BotStartedEvent(
        message_id=UUID("12345678-1234-5678-1234-567812345678"),
        trace_id="trace-1",
        timestamp=1_700_000_000_000,
    )


def test_build_payload_excludes_envelope_metadata():
    event = CommandFailedEvent(command_name="RunBotCommand", error="Ошибка")
    assert NatsPublisher.build_payload(event) == {
        "command_name": "RunBotCommand", "error": "Ошибка"
    }


def test_build_payload_for_empty_event(started_event):
    assert NatsPublisher.build_payload(started_event) == {}


def test_encodes_started_event_with_subject_and_metadata(publisher, started_event):
    subject, message = publisher.encode_event(started_event)

    assert subject == "bot.ABCDEFGHJKMNPQRS.to.control.event.V1.lifecycle.BotStartedEvent"
    assert isinstance(message, BotStartedEvMsg)
    assert message.bot_id == "ABCDEFGHJKMNPQRS"
    assert message.bot_status == "started"
    assert message.message.message_id == str(started_event.message_id)
    assert message.message.trace_id == "trace-1"
    assert message.timestamp == 1_700_000_000_000
    assert message.payload.model_dump() == {}


def test_encodes_failed_command_payload(publisher):
    event = CommandFailedEvent(
        trace_id="trace-failed", command_name="RunBotCommand", error="Ошибка"
    )
    subject, message = publisher.encode_event(event)

    assert subject == "bot.ABCDEFGHJKMNPQRS.to.control.event.V1.failed.CommandFailedEvent"
    assert isinstance(message, CommandFailedEvMsg)
    assert message.message.trace_id == "trace-failed"
    assert message.payload.model_dump() == {
        "command_name": "RunBotCommand", "error": "Ошибка"
    }


def test_encoding_uses_current_runtime_state(publisher, started_event):
    publisher.general_state.bot_status = LifecycleStatus.RUNNING
    _, message = publisher.encode_event(started_event)
    assert message.bot_status == "running"


def test_rejects_unregistered_event(publisher):
    with pytest.raises(RuntimeError, match="Event"):
        publisher.encode_event(Event())


def test_publishes_utf8_json_to_configured_stream(publisher):
    event = CommandFailedEvent(command_name="RunBotCommand", error="Ошибка")
    asyncio.run(publisher.publish_event(event))

    publisher.jetstream.publish.assert_awaited_once()
    kwargs = publisher.jetstream.publish.await_args.kwargs
    assert kwargs["stream"] == "BOT_EVENTS"
    assert kwargs["subject"] == (
        "bot.ABCDEFGHJKMNPQRS.to.control.event.V1.failed.CommandFailedEvent"
    )
    assert isinstance(kwargs["payload"], bytes)
    payload = json.loads(kwargs["payload"].decode("utf-8"))
    assert payload["payload"] == {"command_name": "RunBotCommand", "error": "Ошибка"}
    assert payload["message"]["message_id"] == str(event.message_id)
    assert payload["message"]["trace_id"] == event.trace_id
    assert payload["timestamp"] == event.timestamp


def test_propagates_transport_failure(publisher, started_event):
    error = TimeoutError("publish timeout")
    publisher.jetstream.publish.side_effect = error
    with pytest.raises(TimeoutError) as caught:
        asyncio.run(publisher.publish_event(started_event))
    assert caught.value is error


def test_invalid_event_is_not_published(publisher):
    with pytest.raises(RuntimeError):
        asyncio.run(publisher.publish_event(Event()))
    publisher.jetstream.publish.assert_not_awaited()
