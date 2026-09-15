import asyncio
import logging
import signal


logger = logging.getLogger(__name__)


class ProcessLifecycle:
    def __init__(self) -> None:
        self._shutdown_event = asyncio.Event()

    async def wait_for_shutdown(self) -> None:
        loop = asyncio.get_running_loop()
        shutdown_signals = (signal.SIGINT, signal.SIGTERM)

        logger.debug("Registering process shutdown handlers")

        for shutdown_signal in shutdown_signals:
            loop.add_signal_handler(
                shutdown_signal,
                self._handle_shutdown_signal,
                shutdown_signal,
            )

        logger.info("Process is waiting for a shutdown signal")

        try:
            await self._shutdown_event.wait()
        finally:
            for shutdown_signal in shutdown_signals:
                loop.remove_signal_handler(shutdown_signal)

            logger.debug("Process shutdown handlers removed")

    def _handle_shutdown_signal(
        self,
        shutdown_signal: signal.Signals,
    ) -> None:
        logger.info(
            "Shutdown signal received signal=%s",
            shutdown_signal.name,
        )
        self._shutdown_event.set()
