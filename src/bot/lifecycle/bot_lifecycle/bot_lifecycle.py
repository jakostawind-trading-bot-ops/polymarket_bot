from bot.state import State

from bot.lifecycle.bot_lifecycle.statuses import LifecycleStatuses 

class BotLifecycle():
    def __init__(self,
                 state: State):
        self.state = state
        
    def ensure_status(self, *allowed: LifecycleStatuses):
        if self.state.bot_status not in allowed:
            raise RuntimeError("Invalid bot_status")
        
    async def change_status(self,
                            *allowed_statuses: LifecycleStatuses,
                            new_status: LifecycleStatuses):
        await self.ensure_status(allowed_statuses)
        self.state.bot_status = new_status
        
    
        
        
        