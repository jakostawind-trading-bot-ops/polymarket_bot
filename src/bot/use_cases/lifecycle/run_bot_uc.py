import logging

from bot.lifecycle.lifecycle import Lifecycle
from bot.ports.event_publisher import EventPublisher
from bot.state.general_state import GeneralState
from bot.events.lifecycle_ev import BotRunnedEvent

logger = logging.getLogger(__name__)

class RunBotUc():
    def __init__(self,
                 general_state: GeneralState,
                 lifecycle: Lifecycle,
                 publisher_port: EventPublisher):
        self.general_state = general_state
        self.lifecycle = lifecycle
        self.publisher = publisher_port
        
    async def execute(self):
        prev_status = self.general_state.bot_status.value
        
        # смена режима
        try:
            await self.lifecycle.run()
        
        except Exception as e:
            logger.exception("Не удалось сменить статус")
            return
        
        event = BotRunnedEvent(
            previous_status=prev_status,
            current_status=self.general_state.bot_status.value,
        )
        
        # публикация ивента
        try:
            await self.publisher.publish_event(event)
        except Exception:
            logger.exception("Не удалось опубликовать ивент")