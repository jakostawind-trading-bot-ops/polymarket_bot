from bot.lifecycle.bot_lifecycle.lifecycle import Lifecycle
from bot.events.lifecycle_ev import BotStartedEvent
from bot.ports.event_publisher import EventPublisher
from bot.state.general_state import GeneralState

class StartBotUC():
    def __init__(self,
                 state: GeneralState,
                 bot_lifecycle: Lifecycle,
                 publisher: EventPublisher):
        self.state = state
        self.bot_lifecycle = bot_lifecycle
        self.publisher = publisher
        
    async def execute(self):        
        await self.publisher.publish(BotStartedEvent(
            payload=[],
            msg="Bot started"
        ))