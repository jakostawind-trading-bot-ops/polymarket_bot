import asyncio

from bot.bootstrap import parse_cli_args
from bot.di.container import create_container
from bot.lifecycle.process_lifecycle.process_lifecycle import ProcessLifecycle
from bot.use_cases.lifecycle_uc import StartBotUC


async def main() -> None:
    settings = parse_cli_args()

    async with create_container(settings) as container:
        
        start_bot_use_case = await container.get(StartBotUC)
        process_lifecycle = ProcessLifecycle()
        
        await start_bot_use_case.execute()
        await process_lifecycle.wait_for_shutdown()


if __name__ == "__main__":
    asyncio.run(main())