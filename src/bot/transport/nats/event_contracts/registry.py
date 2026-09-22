from bot.events.failed_ev import CommandFailedEvent
from bot.events.lifecycle_ev import BotStartedEvent, BotRunnedEvent
from bot.events.trading_state_ev import TrackingMarketAddedEvent

from nats_contracts.bot.control.v1.failed.command_failed_ev import CommandFailedEvMsg
from nats_contracts.bot.control.v1.lifecycle import BotStartedEvMsg, BotRunnedEvMsg
from nats_contracts.bot.control.v1.trading_state import TrackingMarketAddedEvMsg

EVENT_CONTRACTS = {
    # failed
    CommandFailedEvent: CommandFailedEvMsg,
    
    # lifecycle
    BotStartedEvent: BotStartedEvMsg,
    BotRunnedEvent: BotRunnedEvMsg,
    
    # trading state
    TrackingMarketAddedEvent: TrackingMarketAddedEvMsg
}