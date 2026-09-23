import logging

from bot.lifecycle.lifecycle import Lifecycle
from bot.ports.event_publisher import EventPublisher
from bot.state.general_state import GeneralState
from bot.events.lifecycle_ev import BotStartedEvent

logger = logging.getLogger(__name__)


class StartBotUC():
    def __init__(self,
                 general_state: GeneralState,
                 lifecycle: Lifecycle,
                 publisher_port: EventPublisher):
        self.general_state = general_state
        self.lifecycle = lifecycle
        self.publisher = publisher_port
        
    async def execute(self):
        logger.info(
            "Начало инициализации бота bot_id=%s status=%s",
            self.general_state.bot_id,
            self.general_state.bot_status.value,
        )

        await self.publisher.publish_event(BotStartedEvent())

        logger.info(
            "Инициализация бота завершена bot_id=%s status=%s",
            self.general_state.bot_id,
            self.general_state.bot_status.value,
        )
