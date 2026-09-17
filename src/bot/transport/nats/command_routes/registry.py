from bot.transport.nats.decoder import CommandRoute

from bot.commands.lifecycle_cmds.run_bot_cmd import RunBotCommand
from bot.commands.state_cmds.account_state.add_account_state_cmd import AddAccountStateCommand
from bot.commands.state_cmds.trading_state.add_tracking_market_cmd import AddTrackingMarketCommand


from nats_contracts.control.bot.v1.lifecycle import RunBotCmdMsg
from nats_contracts.control.bot.v1.account_state import AddAccountStateCmdMsg
from nats_contracts.control.bot.v1.trading_state import AddTrackingMarketCmdMsg

COMMAND_ROUTES = (
    # lifecycle
    CommandRoute(
        msg_type=RunBotCmdMsg.subject_suffix(),
        msg_model=RunBotCmdMsg,
        command_model=RunBotCommand
    ),
    
    # account state
    CommandRoute(
        msg_type=AddAccountStateCmdMsg.subject_suffix(),
        msg_model=AddAccountStateCmdMsg,
        command_model=AddAccountStateCommand
    ),
    
    # tradind state
    CommandRoute(
        msg_type=AddTrackingMarketCmdMsg.subject_suffix(),
        msg_model=AddTrackingMarketCmdMsg,
        command_model=AddTrackingMarketCommand
    )
)
