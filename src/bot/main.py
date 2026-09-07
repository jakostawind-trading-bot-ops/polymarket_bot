import asyncio

from bot.broker.nats.client import NatsClient
from bot.broker.nats.publisher import NatsPublisher

async def main():
    nats_client = await NatsClient.create_nats_client(url="nats://localhost:4222")
    nats_publisher = NatsPublisher(nats_client)
    
    await nats_publisher.publish("bot_test", {"bot_it": "1234565789ABC"})
    


if __name__ == "__main__":
    asyncio.run(main())
