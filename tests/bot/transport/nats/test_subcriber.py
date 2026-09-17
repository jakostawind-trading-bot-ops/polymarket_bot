import asyncio
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest
from nats.aio.msg import Msg
from nats.js.client import JetStreamContext

from bot.commands.dispatcher import CommandDispatcher
from bot.commands.lifecycle_cmds.run_bot_cmd import RunBotCommand
from bot.events.failed_ev import CommandFailedEvent
from bot.transport.nats.command_routes.registry import COMMAND_ROUTES
from bot.transport.nats.decoder import CommandDecodeError, CommandDecoder
from bot.transport.nats.subcriber import NatsSubscriber
from bot.ports.event_publisher import EventPublisher


PREFIX = "control.to.bot.ABCDEFGHJKMNPQRS.command.V1."


@pytest.fixture
def context():
    jetstream = AsyncMock(spec=JetStreamContext)
    subscription = SimpleNamespace(unsubscribe=AsyncMock())
    jetstream.subscribe.return_value = subscription
    dispatcher = AsyncMock(spec=CommandDispatcher)
    publisher = AsyncMock(spec=EventPublisher)
    subscriber = NatsSubscriber(
        jetstream, "BOT_COMMANDS", PREFIX, "bot-consumer",
        CommandDecoder(COMMAND_ROUTES), dispatcher, publisher,
    )
    return SimpleNamespace(
        subscriber=subscriber, jetstream=jetstream, subscription=subscription,
        dispatcher=dispatcher, publisher=publisher,
    )


@pytest.fixture
def message():
    message = Mock(spec=Msg)
    message.subject = PREFIX + "lifecycle.RunBotCommand"
    message.data = json.dumps({
        "bot_id": "ABCDEFGHJKMNPQRS",
        "message": {"message_id": "message-1", "trace_id": "trace-1"},
        "payload": {},
        "timestamp": 1_700_000_000_000,
    }).encode()
    message.ack = AsyncMock()
    message.term = AsyncMock()
    return message


async def deliver(context, message):
    await context.subscriber.start()
    callback = context.jetstream.subscribe.await_args.kwargs["cb"]
    await callback(message)


def test_subscribes_with_durable_consumer_and_manual_ack(context):
    asyncio.run(context.subscriber.start())
    context.jetstream.subscribe.assert_awaited_once()
    kwargs = context.jetstream.subscribe.await_args.kwargs
    assert kwargs["subject"] == PREFIX + ">"
    assert kwargs["stream"] == "BOT_COMMANDS"
    assert kwargs["durable"] == "bot-consumer"
    assert kwargs["manual_ack"] is True
    assert callable(kwargs["cb"])


def test_close_before_start_is_noop(context):
    asyncio.run(context.subscriber.close())
    context.subscription.unsubscribe.assert_not_awaited()


def test_close_unsubscribes_once(context):
    async def scenario():
        await context.subscriber.start()
        await context.subscriber.close()
        await context.subscriber.close()

    asyncio.run(scenario())
    context.subscription.unsubscribe.assert_awaited_once()


def test_successful_command_is_acked_only_after_dispatch(context, message):
    async def dispatch(command):
        assert command == RunBotCommand(trace_id="trace-1")
        message.ack.assert_not_awaited()
        message.term.assert_not_awaited()

    context.dispatcher.dispatch.side_effect = dispatch
    asyncio.run(deliver(context, message))

    context.dispatcher.dispatch.assert_awaited_once_with(RunBotCommand("trace-1"))
    message.ack.assert_awaited_once()
    message.term.assert_not_awaited()
    context.publisher.publish_event.assert_not_awaited()


@pytest.mark.parametrize("subject", ["wrong.subject", PREFIX, PREFIX + "unknown.Command"])
def test_invalid_subject_is_terminated_without_dispatch(context, message, subject):
    message.subject = subject
    asyncio.run(deliver(context, message))
    message.term.assert_awaited_once()
    message.ack.assert_not_awaited()
    context.dispatcher.dispatch.assert_not_awaited()
    context.publisher.publish_event.assert_not_awaited()


@pytest.mark.parametrize("data", [b"{", b"{}"])
def test_invalid_payload_is_terminated(context, message, data):
    message.data = data
    asyncio.run(deliver(context, message))
    message.term.assert_awaited_once()
    message.ack.assert_not_awaited()
    context.dispatcher.dispatch.assert_not_awaited()


@pytest.mark.parametrize("error", [CommandDecodeError("invalid"), RuntimeError("broken route")])
def test_decoder_failure_is_terminated(context, message, error, monkeypatch):
    def fail_decode(*args, **kwargs):
        raise error

    monkeypatch.setattr(CommandDecoder, "decode", fail_decode)
    asyncio.run(deliver(context, message))
    message.term.assert_awaited_once()
    message.ack.assert_not_awaited()
    context.dispatcher.dispatch.assert_not_awaited()
    context.publisher.publish_event.assert_not_awaited()


def test_dispatch_failure_publishes_correlated_event_and_terminates(context, message):
    context.dispatcher.dispatch.side_effect = ValueError("cannot run")
    asyncio.run(deliver(context, message))

    context.publisher.publish_event.assert_awaited_once()
    event = context.publisher.publish_event.await_args.args[0]
    assert isinstance(event, CommandFailedEvent)
    assert event.trace_id == "trace-1"
    assert event.command_name == "RunBotCommand"
    assert event.error == "ValueError: cannot run"
    message.term.assert_awaited_once()
    message.ack.assert_not_awaited()


def test_failure_event_publish_error_still_terminates_delivery(context, message):
    context.dispatcher.dispatch.side_effect = ValueError("cannot run")
    context.publisher.publish_event.side_effect = TimeoutError("publish timeout")
    asyncio.run(deliver(context, message))
    context.publisher.publish_event.assert_awaited_once()
    message.term.assert_awaited_once()
    message.ack.assert_not_awaited()


def test_ack_failure_propagates_without_reporting_command_failure(context, message):
    message.ack.side_effect = TimeoutError("ack timeout")
    with pytest.raises(TimeoutError, match="ack timeout"):
        asyncio.run(deliver(context, message))
    context.dispatcher.dispatch.assert_awaited_once()
    context.publisher.publish_event.assert_not_awaited()
    message.term.assert_not_awaited()


def test_subscription_failure_propagates(context):
    context.jetstream.subscribe.side_effect = TimeoutError("subscribe timeout")
    with pytest.raises(TimeoutError, match="subscribe timeout"):
        asyncio.run(context.subscriber.start())
