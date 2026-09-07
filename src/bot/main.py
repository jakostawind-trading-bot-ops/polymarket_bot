import asyncio

from bot.bootstrap import parse_cli_args
from bot.nats.publisher import NatsPublisher
from bot.di.container import create_container
from bot.lifecycle.process_lifecycle.process_lifecycle import ProcessLifecycle


async def main() -> None:
    settings = parse_cli_args()

    async with create_container(settings) as container:
        publisher = await container.get(NatsPublisher)
        
        process_lifecycle = ProcessLifecycle()

        await publisher.publish(
            subject="bot_test",
            message={"bot_id": "1234565789ABC"},
        )
        
        await process_lifecycle.wait_for_shutdown()


if __name__ == "__main__":
    asyncio.run(main())
    main()
