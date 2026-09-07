import asyncio

from bot.bootstrap import BootstrapSettings, parse_cli_args
from bot.nats.publisher import NatsPublisher
from bot.di.container import create_container
from bot.lifecycle.process_lifecycle.process_lifecycle import ProcessLifecycle


async def run(bootstrap_settings: BootstrapSettings) -> None:
    async with create_container(bootstrap_settings) as container:
        publisher = await container.get(NatsPublisher)
        
        process_lifecycle = ProcessLifecycle()

        await publisher.publish(
            subject="bot_test",
            message={"bot_id": "1234565789ABC"},
        )
        
        await process_lifecycle.wait_for_shutdown()


def main() -> None:
    settings = parse_cli_args()
    asyncio.run(run(settings))


if __name__ == "__main__":
    main()
