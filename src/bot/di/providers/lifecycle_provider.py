from dishka import provide, Provider, Scope

from bot.lifecycle.bot_lifecycle.bot_lifecycle import BotLifecycle
from bot.lifecycle.bot_lifecycle.statuses import LifecycleStatuses
from bot.state import State, generate_bet_id

class LifecycleProvider(Provider):
    scope = Scope.APP
    
    @provide
    def provide_state(self) -> State:
        return State(
            bot_id=generate_bet_id(),
            bot_status=LifecycleStatuses.STARTED
        )
    
    bot_lifecycle = provide(BotLifecycle)