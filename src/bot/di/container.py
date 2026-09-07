from dishka import make_async_container

from bot.bootstrap import BootstrapSettings
from bot.di.providers.bootstrap_provider import BootstrapSettingsProvider
from bot.di.providers.nats_provider import NatsProvider

def create_container(bootstrap_settings: BootstrapSettings):
    return make_async_container(
        BootstrapSettingsProvider(),
        NatsProvider(),
        context={BootstrapSettings: bootstrap_settings}
    )