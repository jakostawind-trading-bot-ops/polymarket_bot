from bot.commands.lifecycle.run_bot import RunBotCommand, RunBotSchema
from bot.nats.decoder import CommandRoute


COMMAND_ROUTES = (
    CommandRoute(
        message_type="lifecycle.run",
        command_type=RunBotCommand,
        payload_schema=RunBotSchema
    ),
)
