import asyncio

from bot.bootstrap import BootstrapSettings, parse_cli_args
from bot.nats.publisher import NatsPublisher
from bot.di.container import create_container


async def run(bootstrap_settings: BootstrapSettings) -> None:
    async with create_container(bootstrap_settings) as container:
        publisher = await container.get(NatsPublisher)

        await publisher.publish(
            subject="bot_test",
            message={"bot_id": "1234565789ABC"},
        )


def main() -> None:
    settings = parse_cli_args()
    asyncio.run(run(settings))


if __name__ == "__main__":
    main()
