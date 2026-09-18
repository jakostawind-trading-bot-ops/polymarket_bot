import asyncio
import logging

from bot.logging_config import configure_logging
from bot.bootstrap import parse_cli_args
from bot.di.container import create_container
from bot.process_lifecycle import ProcessLifecycle
from bot.ports.command_subscriber import CommandSubscriber
from bot.use_cases.lifecycle.start_bot_uc import StartBotUC


logger = logging.getLogger(__name__)


async def main() -> None:
    settings = parse_cli_args()
    logger.info("Запуск процесса бота")

    async with create_container(settings) as container:
        await container.get(CommandSubscriber)
        logger.info("Transport команд инициализирован")

        start_bot_use_case = await container.get(StartBotUC)
        process_lifecycle = ProcessLifecycle()

        await start_bot_use_case.execute()
        logger.info(
            "Use case запуска бота завершён; ожидание shutdown"
        )

        await process_lifecycle.wait_for_shutdown()
        logger.info("Запрошен shutdown; закрытие ресурсов приложения")

    logger.info("Процесс бота остановлен")


if __name__ == "__main__":
    configure_logging()
    asyncio.run(main())
