import secrets

from bot.nats.publisher import NatsPublisher
from bot.state import State
from bot.lifecycle.bot_lifecycle.bot_lifecycle import BotLifecycle, LifecycleStatuses

class StartBotUC():
    def __init__(self,
                 state: State,
                 bot_lifecycle: BotLifecycle,
                 publisher: NatsPublisher):
        self.state = state
        self.bot_lifecycle = BotLifecycle
        self.publisher = publisher
        
    async def execute(self):        
        await self.publisher.publish(
            subject="bot_test",
            message={
                "bot_id": self.state.bot_id,
                "bot_status": self.state.bot_status
            }
        )