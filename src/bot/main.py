import asyncio
import logging

from bot.logging_config import configure_logging
from bot.bootstrap import parse_cli_args
from bot.di.container import create_container
from bot.process_lifecycle import ProcessLifecycle
from bot.ports.command_subscriber import CommandSubscriber
from bot.use_cases.lifecycle_uc import StartBotUC


logger = logging.getLogger(__name__)


async def main() -> None:
    settings = parse_cli_args()
    logger.info("Bot process starting")

    async with create_container(settings) as container:
        await container.get(CommandSubscriber)
        logger.info("Command transport initialized")

        start_bot_use_case = await container.get(StartBotUC)
        process_lifecycle = ProcessLifecycle()

        await start_bot_use_case.execute()
        logger.info(
            "Bot startup use case completed; waiting for shutdown"
        )

        await process_lifecycle.wait_for_shutdown()
        logger.info("Shutdown requested; closing application resources")

    logger.info("Bot process stopped")


if __name__ == "__main__":
    configure_logging()
    asyncio.run(main())
