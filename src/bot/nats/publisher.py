import json
from nats.aio.client import Client

class NatsPublisher():
    def __init__(self, nats_client: Client):
        self.nats_client = nats_client
    
    async def publish(self, subject: str, message: dict):
        await self.nats_client.publish(
            subject=subject,
            payload=json.dumps(message).encode()
        )