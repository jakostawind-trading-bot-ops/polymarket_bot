from bot.nats.decoder import CommandRoute

from bot.commands.lifecycle_cmds.run_bot_cmd import RunBotCommand

from bot.commands.state_cmds.polymarket_state.add_polymarket_state_cmd import AddPolymarketStateCommand


from nats_contracts.control.bot.v1.lifecycle import RunBotCmdMsg
from nats_contracts.control.bot.v1.state import AddPolymarketStateCmdMsg

COMMAND_ROUTES = (
    # lifecycle
    CommandRoute(
        msg_type="lifecycle.RunBotCommand",
        msg_model=RunBotCmdMsg,
        command_model=RunBotCommand
    ),
    
    # state
    CommandRoute(
        msg_type="state.AddPolymarketStateCommand",
        msg_model=AddPolymarketStateCmdMsg,
        command_model=AddPolymarketStateCommand
    )
)
