from bot.events import (
    CommandFailedEvent,
    BotStartedEvent,
    BotRunnedEvent,
    TrackingMarketAddedEvent,
    TrackingMarketRemovedEvent
)

from nats_contracts.bot.control.v1 import (
    CommandFailedEvMsg,
    BotStartedEvMsg,
    BotRunnedEvMsg,
    TrackingMarketAddedEvMsg,
    TrackingMarketRemovedEvMsg
)

EVENT_CONTRACTS = {
    # failed
    CommandFailedEvent: CommandFailedEvMsg,
    
    # lifecycle
    BotStartedEvent: BotStartedEvMsg,
    BotRunnedEvent: BotRunnedEvMsg,
    
    # trading state
    TrackingMarketAddedEvent: TrackingMarketAddedEvMsg,
    TrackingMarketRemovedEvent: TrackingMarketRemovedEvMsg
}