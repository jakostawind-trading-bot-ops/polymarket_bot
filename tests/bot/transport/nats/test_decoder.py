import json

import pytest
from pydantic import ValidationError

from bot.commands.lifecycle_cmds.run_bot_cmd import RunBotCommand
from bot.commands.state_cmds.polymarket_state.add_polymarket_state_cmd import AddPolymarketStateCommand
from bot.transport.nats.command_routes.registry import COMMAND_ROUTES
from bot.transport.nats.decoder import CommandDecodeError, CommandDecoder, CommandRoute


@pytest.fixture
def state_message():
    return {
        "bot_id": "ABCDEFGHJKMNPQRS",
        "message": {
            "message_id": "message-1",
            "trace_id": "trace-1",
            "message_type": "state",
            "message_name": "AddPolymarketStateCommand",
        },
        "payload": {"nickname": "трейдер", "wallet": "wallet-1"},
        "timestamp": 1_700_000_000_000,
    }


def test_decodes_state_command_payload_and_trace_id(state_message):
    decoder = CommandDecoder(iter(COMMAND_ROUTES))

    command = decoder.decode(
        "state.AddPolymarketStateCommand",
        json.dumps(state_message, ensure_ascii=False).encode("utf-8"),
    )

    assert command == AddPolymarketStateCommand(
        trace_id="trace-1", nickname="трейдер", wallet="wallet-1"
    )


def test_decodes_lifecycle_command_with_empty_payload(state_message):
    state_message["message"].update(
        message_type="lifecycle", message_name="RunBotCommand"
    )
    state_message["payload"] = {}

    command = CommandDecoder(COMMAND_ROUTES).decode(
        "lifecycle.RunBotCommand", json.dumps(state_message).encode()
    )

    assert command == RunBotCommand(trace_id="trace-1")


def test_rejects_duplicate_routes():
    route = COMMAND_ROUTES[0]
    with pytest.raises(RuntimeError, match="Duplicate command route"):
        CommandDecoder([route, route])


@pytest.mark.parametrize("routes", [(), COMMAND_ROUTES])
def test_rejects_unknown_command_type(routes):
    with pytest.raises(CommandDecodeError, match="Unsupported command type"):
        CommandDecoder(routes).decode("unknown.Command", b"{}")


@pytest.mark.parametrize("raw_message", [b"", b"{", b"\xff", b"null", b"[]", b"{}"])
def test_wraps_invalid_json_or_contract_in_decode_error(raw_message):
    with pytest.raises(CommandDecodeError) as caught:
        CommandDecoder(COMMAND_ROUTES).decode(
            "state.AddPolymarketStateCommand", raw_message
        )

    assert isinstance(caught.value.__cause__, ValidationError)


@pytest.mark.parametrize("field", ["nickname", "wallet"])
def test_rejects_missing_payload_fields(state_message, field):
    del state_message["payload"][field]
    with pytest.raises(CommandDecodeError):
        CommandDecoder(COMMAND_ROUTES).decode(
            "state.AddPolymarketStateCommand", json.dumps(state_message).encode()
        )


def test_rejects_contract_for_different_route(state_message):
    with pytest.raises(CommandDecodeError):
        CommandDecoder(COMMAND_ROUTES).decode(
            "lifecycle.RunBotCommand", json.dumps(state_message).encode()
        )


def test_reports_incompatible_internal_command_as_programming_error(state_message):
    state_route = COMMAND_ROUTES[1]
    decoder = CommandDecoder([
        CommandRoute(state_route.msg_type, state_route.msg_model, RunBotCommand)
    ])

    with pytest.raises(RuntimeError, match="payload does not match command") as caught:
        decoder.decode(state_route.msg_type, json.dumps(state_message).encode())

    assert isinstance(caught.value.__cause__, TypeError)
