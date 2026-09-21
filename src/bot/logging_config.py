import logging
import logging.config
import logging.handlers
import time

from datetime import datetime, timedelta, timezone
from pathlib import Path


class FiveMinuteFileHandler(logging.Handler):
    def __init__(self, directory: str = "logs") -> None:
        super().__init__()

        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

        self._bucket_start: datetime | None = None
        self._stream = None

    def emit(self, record: logging.LogRecord) -> None:
        try:
            record_time = datetime.fromtimestamp(
                record.created,
                tz=timezone.utc,
            )

            bucket_start = record_time.replace(
                minute=(record_time.minute // 5) * 5,
                second=0,
                microsecond=0,
            )

            if bucket_start != self._bucket_start:
                self._switch_file(bucket_start)

            message = self.format(record)

            self._stream.write(message + "\n")
            self._stream.flush()

        except Exception:
            self.handleError(record)

    def _switch_file(self, bucket_start: datetime) -> None:
        if self._stream is not None:
            self._stream.close()

        bucket_end = bucket_start + timedelta(minutes=5)

        filename = (
            f"{bucket_start:%Y-%m-%d-%H:%M}-"
            f"{bucket_end:%H:%M}.log"
        )

        self._stream = (self.directory / filename).open(
            mode="a",
            encoding="utf-8",
        )

        self._bucket_start = bucket_start

    def close(self) -> None:
        if self._stream is not None:
            self._stream.close()
            self._stream = None

        super().close()


def configure_logging(level: str = "INFO") -> None:
    logging.Formatter.converter = time.gmtime

    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,

        "formatters": {
            "standard": {
                "format": (
                    "%(asctime)s.%(msecs)03dZ | "
                    "%(levelname)-8s | "
                    "%(name)s | "
                    "%(filename)s:%(lineno)d | "
                    "%(funcName)s | "
                    "%(message)s"
                ),
                "datefmt": "%Y-%m-%dT%H:%M:%S",
            },
        },

        "handlers": {
            "file": {
                "()": FiveMinuteFileHandler,
                "directory": "logs",
                "formatter": "standard",
            },

            "queue": {
                "class": "logging.handlers.QueueHandler",
                "handlers": ["file"],
                "respect_handler_level": True,
            },
        },

        "root": {
            "level": level,
            "handlers": ["queue"],
        },
    })

    queue_handler = logging.getHandlerByName("queue")

    if queue_handler.listener is not None:
        queue_handler.listener.start()


def shutdown_logging() -> None:
    queue_handler = logging.getHandlerByName("queue")

    if (
        queue_handler is not None
        and queue_handler.listener is not None
    ):
        queue_handler.listener.stop()

    logging.shutdown()