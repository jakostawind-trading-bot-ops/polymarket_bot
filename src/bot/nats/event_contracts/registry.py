from bot.events.failed_ev import CommandFailedEvent
from bot.events.lifecycle_ev import BotStartedEvent

from nats_contracts.bot.control.v1.failed.command_failed_ev import CommandFailedEvMsg
from nats_contracts.bot.control.v1.lifecycle import BotStartedEvMsg

EVENT_CONTRACTS = {
    # failed
    CommandFailedEvent: CommandFailedEvMsg,
    
    # lifecycle
    BotStartedEvent: BotStartedEvMsg
}