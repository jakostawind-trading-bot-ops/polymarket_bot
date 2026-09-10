import logging

from nats.aio.msg import Msg
from nats.js.client import JetStreamContext

from bot.commands.dispatcher import CommandDispatcher
from bot.nats.decoder import CommandDecodeError, CommandDecoder


logger = logging.getLogger(__name__)


class NatsSubscriber:
    def __init__(
        self,
        jetstream: JetStreamContext,
        stream_name: str,
        subject_prefix: str,
        consumer_name: str,
        decoder: CommandDecoder,
        dispatcher: CommandDispatcher,
    ) -> None:
        self._jetstream = jetstream
        self._stream_name = stream_name
        self._subject_prefix = subject_prefix
        self._consumer_name = consumer_name
        self._decoder = decoder
        self._dispatcher = dispatcher
        self._subscription = None

    async def start(self) -> None:
        self._subscription = await self._jetstream.subscribe(
            subject=f"{self._subject_prefix}>",
            durable = self._consumer_name,
            cb=self._handle_message,
            manual_ack=True,
        )

    async def close(self) -> None:
        if self._subscription is not None:
            await self._subscription.unsubscribe()
            self._subscription = None

    async def _handle_message(self, message: Msg) -> None:
        try:
            message_type = self._extract_message_type(
                message.subject,
            )

            command = self._decoder.decode(
                message_type=message_type,
                raw_message=message.data,
            )
        except CommandDecodeError as error:
            logger.warning(
                "Invalid command on subject %s: %s",
                message.subject,
                error,
            )
            await message.ack()
            return
        except Exception:
            logger.exception(
                "Command decoding failed on subject %s",
                message.subject,
            )
            await message.nak()
            return

        try:
            await self._dispatcher.dispatch(command)
        except Exception:
            logger.exception(
                "Command processing failed on subject %s",
                message.subject,
            )
            await message.nak()
            return

        await message.ack()

    def _extract_message_type(self, subject: str) -> str:
        if not subject.startswith(self._subject_prefix):
            raise CommandDecodeError(
                f"Unexpected subject: {subject}"
            )

        message_type = subject.removeprefix(
            self._subject_prefix,
        )

        if not message_type:
            raise CommandDecodeError("Missing command type")

        return message_type
