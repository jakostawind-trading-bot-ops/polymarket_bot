from bot.lifecycle.bot_lifecycle.lifecycle import Lifecycle
from bot.ports.event_publisher import EventPublisher
from bot.state.general_state import GeneralState
from bot.events.lifecycle_ev import BotStartedEvent, BotRunnedEvent


class StartBotUC():
    def __init__(self,
                 general_state: GeneralState,
                 lifecycle: Lifecycle,
                 publisher: EventPublisher):
        self.general_state = general_state
        self.lifecycle = lifecycle
        self.publisher = publisher
        
    async def execute(self):        
        await self.publisher.publish_event(BotStartedEvent(
            payload=[],
            msg="Bot started"
        ))
        
class RunBotUC():
    def __init__(self,
                 general_state: GeneralState,
                 lifecycle: Lifecycle,
                 publisher: EventPublisher):
        self.general_state = general_state
        self.lifecycle = lifecycle
        self.publisher = publisher
        
    async def execute(self):
        prev_status = self.general_state.bot_status
        await self.publisher.publish_event(BotRunnedEvent(
            payload={
                "prev_status": prev_status,
                "cur_status": self.general_state.bot_status
            },
            msg="Bot runned"
        ))