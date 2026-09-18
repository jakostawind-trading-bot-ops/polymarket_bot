import logging

from nats.aio.msg import Msg
from nats.js.client import JetStreamContext

from bot.commands.dispatcher import CommandDispatcher
from bot.events.failed_ev import CommandFailedEvent
from bot.transport.nats.decoder import CommandDecodeError, CommandDecoder
from bot.ports.event_publisher import EventPublisher


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
        publisher: EventPublisher,
    ) -> None:
        self._jetstream = jetstream
        self._stream_name = stream_name
        self._subject_prefix = subject_prefix
        self._consumer_name = consumer_name
        self._decoder = decoder
        self._dispatcher = dispatcher
        self._publisher = publisher
        self._subscription = None

    async def start(self) -> None:
        subject = f"{self._subject_prefix}>"
        logger.info(
            "Запуск NATS subscriber команд "
            "stream=%s consumer=%s subject=%s",
            self._stream_name,
            self._consumer_name,
            subject,
        )

        self._subscription = await self._jetstream.subscribe(
            subject=subject,
            durable=self._consumer_name,
            stream=self._stream_name,
            cb=self._handle_message,
            manual_ack=True,
        )

        logger.info(
            "NATS subscriber команд запущен consumer=%s",
            self._consumer_name,
        )

    async def close(self) -> None:
        if self._subscription is None:
            logger.debug(
                "NATS subscriber команд уже остановлен "
                "consumer=%s",
                self._consumer_name,
            )
            return

        logger.info(
            "Остановка NATS subscriber команд consumer=%s",
            self._consumer_name,
        )

        await self._subscription.unsubscribe()
        self._subscription = None

        logger.info(
            "NATS subscriber команд остановлен consumer=%s",
            self._consumer_name,
        )

    async def _handle_message(self, message: Msg) -> None:
        logger.debug(
            "Получена команда из NATS subject=%s size_bytes=%d",
            message.subject,
            len(message.data),
        )

        try:
            message_type = self._extract_message_type(
                message.subject,
            )

            command = self._decoder.decode(
                msg_type=message_type,
                raw_message=message.data,
            )

            logger.info(
                "Команда декодирована command=%s trace_id=%s subject=%s",
                type(command).__name__,
                command.trace_id,
                message.subject,
            )
        except CommandDecodeError as error:
            logger.warning(
                "Некорректная команда в subject %s: %s",
                message.subject,
                error,
            )
            await message.term()
            logger.debug(
                "Доставка некорректной команды прекращена subject=%s",
                message.subject,
            )
            return
        except Exception:
            logger.exception(
                "Не удалось декодировать команду в subject %s",
                message.subject,
            )
            await message.term()
            logger.debug(
                "Доставка команды прекращена из-за ошибки subject=%s",
                message.subject,
            )
            return

        try:
            await self._dispatcher.dispatch(command)
        except Exception as error:
            logger.exception(
                "Ошибка обработки команды command=%s trace_id=%s subject=%s",
                type(command).__name__,
                command.trace_id,
                message.subject,
            )
            try:
                await self._publisher.publish_event(
                    CommandFailedEvent(
                        trace_id=command.trace_id,
                        command_name=type(command).__name__,
                        error=f"{type(error).__name__}: {error}",
                    )
                )
            except Exception:
                logger.exception(
                    "Не удалось опубликовать event ошибки команды command=%s trace_id=%s",
                    type(command).__name__,
                    command.trace_id,
                )
            finally:
                await message.term()

            logger.debug(
                "Доставка команды прекращена из-за ошибки "
                "command=%s trace_id=%s",
                type(command).__name__,
                command.trace_id,
            )
            return

        logger.info(
            "Команда обработана command=%s trace_id=%s",
            type(command).__name__,
            command.trace_id,
        )

        await message.ack()
        logger.debug(
            "Для команды отправлен ACK command=%s trace_id=%s",
            type(command).__name__,
            command.trace_id,
        )

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
