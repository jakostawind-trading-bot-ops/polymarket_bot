from bot.commands.lifecycle.run_bot import RunBotCommand
from bot.nats.decoder import CommandRoute


COMMAND_ROUTES = (
    CommandRoute(
        message_type="lifecycle.run",
        command_type=RunBotCommand,
    ),
)
