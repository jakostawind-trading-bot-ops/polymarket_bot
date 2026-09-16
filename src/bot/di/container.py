from dishka import make_async_container

from bot.bootstrap import BootstrapSettings
from bot.di.providers.bootstrap_provider import BootstrapSettingsProvider
from bot.di.providers.nats_provider import NatsProvider
from bot.di.providers.command_provider import CommandProvider
from bot.di.providers.trading_state_provider import TradingStateProvider
from bot.di.providers.lifecycle_provider import LifecycleProvider
from bot.di.providers.use_case_provider import LifecycleUCProvider

def create_container(bootstrap_settings: BootstrapSettings):
    return make_async_container(
        BootstrapSettingsProvider(),
        NatsProvider(),
        LifecycleProvider(),
        CommandProvider(),
        TradingStateProvider(),
        
        # use cases
        LifecycleUCProvider(),
        
        context={BootstrapSettings: bootstrap_settings}
    )