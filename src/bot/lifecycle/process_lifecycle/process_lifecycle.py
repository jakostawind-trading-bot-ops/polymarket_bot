import asyncio
import signal


class ProcessLifecycle:
    def __init__(self) -> None:
        self._shutdown_event = asyncio.Event()

    async def wait_for_shutdown(self) -> None:
        loop = asyncio.get_running_loop()
        shutdown_signals = (signal.SIGINT, signal.SIGTERM)

        for shutdown_signal in shutdown_signals:
            loop.add_signal_handler(
                shutdown_signal,
                self._shutdown_event.set,
            )

        try:
            await self._shutdown_event.wait()
        finally:
            for shutdown_signal in shutdown_signals:
                loop.remove_signal_handler(shutdown_signal)