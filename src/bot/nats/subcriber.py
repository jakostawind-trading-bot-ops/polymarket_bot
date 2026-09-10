from bot.commands.dispatcher import CommandDispatcher
from bot.nats.decoder import CommandDecoder

class NatsSubscriber:
    def __init__(
        self,
        jetstream,
        subject_prefix: str,
        decoder: CommandDecoder,
        dispatcher: CommandDispatcher,
    ) -> None:
        self._jetstream = jetstream
        self._subject_prefix = subject_prefix
        self._decoder = decoder
        self._dispatcher = dispatcher
        self._subscription = None

    async def start(self) -> None:
        self._subscription = await self._jetstream.subscribe(
            subject=f"{self._subject_prefix}>",
            cb=self._handle_message,
            manual_ack=True,
        )

    async def close(self) -> None:
        if self._subscription is not None:
            await self._subscription.unsubscribe()
            self._subscription = None

    async def _handle_message(self, message) -> None:
        try:
            command_type = self._extract_command_type(
                message.subject,
            )

            command = self._decoder.decode(
                command_type=command_type,
                raw_message=message.data,
            )

            await self._dispatcher.dispatch(command)
        except RuntimeError as error:
            print(f"Invalid command: {error}")
            await message.ack()
            return
        except Exception as error:
            print(f"Command processing failed: {error!r}")
            await message.nak()
            return

        await message.ack()

    def _extract_command_type(self, subject: str) -> str:
        if not subject.startswith(self._subject_prefix):
            raise RuntimeError(
                f"Unexpected subject: {subject}"
            )

        command_type = subject.removeprefix(
            self._subject_prefix,
        )

        if not command_type:
            raise RuntimeError("Missing command type")

        return command_type