from collections.abc import AsyncIterator
from dishka import provide, Provider, Scope
import nats
from nats.aio.client import Client

from bot.nats.publisher import NatsPublisher

class NatsProvider(Provider):
    scope = Scope.APP
    
    @provide
    async def provide_nats_client(self) -> AsyncIterator[Client]:
        nc = await nats.connect("nats://localhost:4222")
        try:
            yield nc
        finally:
            await nc.close()
        
    nats_publisher = provide(NatsPublisher)