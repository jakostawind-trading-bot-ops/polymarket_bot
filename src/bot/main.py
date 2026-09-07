import asyncio

from dishka import make_async_container

from bot.bootstrap import BootstrapSettings, parse_cli_args
from bot.di.providers.bootstrap_provider import BootstrapSettingsProvider
from bot.di.providers.nats_provider import NatsProvider
from bot.nats.publisher import NatsPublisher


async def run(settings: BootstrapSettings) -> None:
    async with make_async_container(
        BootstrapSettingsProvider(),
        NatsProvider(),
        context={BootstrapSettings: settings},
    ) as container:
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
