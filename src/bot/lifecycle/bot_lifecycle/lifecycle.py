from bot.state.general_state import GeneralState

from bot.lifecycle.bot_lifecycle.statuses import LifecycleStatuses 

class Lifecycle():
    def __init__(self,
                 general_state: GeneralState):
        self.general_state = general_state
        
    def ensure_status(self, *allowed: LifecycleStatuses):
        if self.state.bot_status not in allowed:
            raise RuntimeError("Invalid bot_status")
        
    async def change_status(self,
                            *allowed_statuses: LifecycleStatuses,
                            new_status: LifecycleStatuses):
        await self.ensure_status(allowed_statuses)
        self.state.bot_status = new_status
        
    async def run(self):
        self.general_state = LifecycleStatuses.RUNNING