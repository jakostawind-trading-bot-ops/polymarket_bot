import asyncio
from dishka import make_async_container

from bot.di.nats_provider import NatsProvider
from bot.nats.publisher import NatsPublisher

async def main():
    async with make_async_container(NatsProvider()) as container:
        publisher = await container.get(NatsPublisher)
        
        await publisher.publish(
            subject="test_bot",
            message={"bot_id": "abc123"}
        )
    


if __name__ == "__main__":
    asyncio.run(main())
