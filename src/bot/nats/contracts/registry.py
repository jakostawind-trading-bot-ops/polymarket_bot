from bot.events.lifecycle_ev import BotStartedEvent

from nats_contracts.bot.v1.control.lifecycle import BotStartedMsg

EVENT_CONTRACTS = {
    BotStartedEvent: BotStartedMsg
}