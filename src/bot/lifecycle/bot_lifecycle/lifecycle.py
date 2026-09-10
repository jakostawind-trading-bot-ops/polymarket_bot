from bot.state.general_state import GeneralState

from bot.lifecycle.bot_lifecycle.statuses import LifecycleStatuses 

class Lifecycle():
    def __init__(self,
                 general_state: GeneralState):
        self.general_state = general_state
        
    def ensure_status(self, *allowed: LifecycleStatuses):
        if self.general_state.bot_status not in allowed:
            allowed_values = ", ".join(status.value for status in allowed)
            raise RuntimeError(
                f"Cannot change status from "
                f"{self.general_state.bot_status.value}; "
                f"allowed statuses: {allowed_values}"
            )
        
    def change_status(self,
                            *allowed_statuses: LifecycleStatuses,
                            new_status: LifecycleStatuses):
        self.ensure_status(*allowed_statuses)
        self.general_state.bot_status = new_status
        
    def run(self):
        self.change_status(
            LifecycleStatuses.STARTED,
            new_status=LifecycleStatuses.RUNNING
        )