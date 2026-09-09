from bot.commands.dispatcher import CommandDispatcher
from bot.nats.decoder import CommandDecoder

class NatsSubscriber:
    def __init__(
        self,
        jetstream,
        subject: str,
        decoder: CommandDecoder,
        dispatcher: CommandDispatcher,
    ) -> None:
        self._jetstream = jetstream
        self._subject = subject
        self._decoder = decoder
        self._dispatcher = dispatcher
        self._subscription = None

    async def start(self) -> None:
        self._subscription = await self._jetstream.subscribe(
            subject=self._subject,
            cb=self._handle_message,
            manual_ack=True,
        )

    async def close(self) -> None:
        if self._subscription is not None:
            await self._subscription.unsubscribe()
            self._subscription = None

    async def _handle_message(self, message) -> None:
        try:
            command = self._decoder.decode(message.data)
            await self._dispatcher.dispatch(command)
        except RuntimeError():
            await message.ack()
            return
        except Exception:
            await message.nak()
            return

        await message.ack()