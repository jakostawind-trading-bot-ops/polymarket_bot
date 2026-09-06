import nats
from nats.aio.client import Client as NATS

class NatsClient():
    
    async def create_nats_client(url: str) -> NATS:
        nc = await nats.connect(url)
        return nc