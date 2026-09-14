from bot.events.lifecycle_ev import BotStartedEvent

from nats_contracts.bot.control.v1.lifecycle import BotStartedEvMsg

EVENT_CONTRACTS = {
    BotStartedEvent: BotStartedEvMsg
}