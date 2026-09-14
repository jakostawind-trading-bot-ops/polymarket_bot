from dishka import provide, Provider, Scope

from bot.lifecycle.bot_lifecycle.lifecycle import Lifecycle
from bot.lifecycle.bot_lifecycle.statuses import LifecycleStatus
from bot.state.general_state import GeneralState, generate_bet_id

class LifecycleProvider(Provider):
    scope = Scope.APP
    
    @provide
    def provide_state(self) -> GeneralState:
        return GeneralState(
            # bot_id=generate_bet_id(),
            bot_id="test_bot", # временно чтобы каждый раз не переключать в натсе
            bot_status=LifecycleStatus.STARTED
        )
    
    bot_lifecycle = provide(Lifecycle)