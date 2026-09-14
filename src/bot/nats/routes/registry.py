from bot.commands.lifecycle_cmds.run_bot_cmd import RunBotCommand
from bot.nats.decoder import CommandRoute

from nats_contracts.control.bot.v1.lifecycle import RunBotCmdMsg

COMMAND_ROUTES = (
    CommandRoute(
        msg_type="lifecycle.RunBotCommand",
        msg_model=RunBotCmdMsg,
        command_model=RunBotCommand
    ),
)
