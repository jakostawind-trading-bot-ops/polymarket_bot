from collections.abc import AsyncIterator
from dishka import provide, Provider, Scope
import nats
from nats.aio.client import Client

from bot.nats.publisher import NatsPublisher
from bot.bootstrap import BootstrapSettings

class NatsProvider(Provider):
    scope = Scope.APP
    
    @provide
    async def provide_nats_client(
        self,
        bootstrap_settings: BootstrapSettings
        ) -> AsyncIterator[Client]:
        nc = await nats.connect(bootstrap_settings.nats_url)
        try:
            yield nc
        finally:
            await nc.close()
        
    nats_publisher = provide(NatsPublisher)