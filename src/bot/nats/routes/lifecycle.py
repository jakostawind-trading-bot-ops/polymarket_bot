from typing import Any

from bot.commands.lifecycle_cmd import RunBotCommand
from bot.commands.command import Command
from bot.nats.decoder import CommandRoute


def decode_run_bot(
    message: dict[str, Any],
) -> RunBotCommand:
    trace_id = message.get("trace_id")

    if not isinstance(trace_id, str):
        raise RuntimeError("Missing or invalid trace_id")

    return RunBotCommand(
        trace_id=trace_id,
    )


LIFECYCLE_ROUTES = (
    CommandRoute(
        message_type="lifecycle.run",
        factory=decode_run_bot,
    ),
)