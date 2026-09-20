from dishka import provide, Provider, Scope

from bot.bootstrap import BootstrapSettings
from bot.lifecycle.bot_lifecycle.lifecycle import Lifecycle
from bot.lifecycle.bot_lifecycle.statuses import LifecycleStatus
from bot.state.general_state import GeneralState, generate_bet_id

class LifecycleProvider(Provider):
    scope = Scope.APP
    
    @provide
    def provide_state(
        self,
        bootstrap_settings: BootstrapSettings
        ) -> GeneralState:
        return GeneralState(
            bot_id=(
                "test_bot"
                if bootstrap_settings.debug
                else generate_bet_id()
            ),
            bot_status=LifecycleStatus.STARTED
        )
    
    bot_lifecycle = provide(Lifecycle)