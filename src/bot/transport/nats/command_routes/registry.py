from bot.transport.nats.decoder import CommandRoute

from bot.commands import (
    RunBotCommand,
    AddTrackingMarketCommand,
    RemoveTrackingMarketCommand
)


from nats_contracts.control.bot.v1 import (
    RunBotCmdMsg,
    AddTrackingMarketCmdMsg,
    RemoveTrackingMarketCmdMsg
)

COMMAND_ROUTES = (
    # lifecycle
    CommandRoute(
        msg_type=RunBotCmdMsg.subject_suffix(),
        msg_model=RunBotCmdMsg,
        command_model=RunBotCommand
    ),
    
    # account state
    # CommandRoute(
    #     msg_type=AddAccountStateCmdMsg.subject_suffix(),
    #     msg_model=AddAccountStateCmdMsg,
    #     command_model=AddAccountStateCommand
    # ),
    
    # tradind state
    CommandRoute(
        msg_type=AddTrackingMarketCmdMsg.subject_suffix(),
        msg_model=AddTrackingMarketCmdMsg,
        command_model=AddTrackingMarketCommand
    ),
    CommandRoute(
        msg_type=RemoveTrackingMarketCmdMsg.subject_suffix(),
        msg_model=RemoveTrackingMarketCmdMsg,
        command_model=RemoveTrackingMarketCommand
    )
)
