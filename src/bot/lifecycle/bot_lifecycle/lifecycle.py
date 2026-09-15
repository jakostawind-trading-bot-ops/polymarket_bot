import logging

from bot.state.general_state import GeneralState

from bot.lifecycle.bot_lifecycle.statuses import LifecycleStatus


logger = logging.getLogger(__name__)


class Lifecycle():
    def __init__(self,
                 general_state: GeneralState):
        self.general_state = general_state
        
    def ensure_status(self, *allowed: LifecycleStatus):
        if self.general_state.bot_status not in allowed:
            allowed_values = ", ".join(status.value for status in allowed)
            raise RuntimeError(
                f"Cannot change status from "
                f"{self.general_state.bot_status.value}; "
                f"allowed statuses: {allowed_values}"
            )
        
    def change_status(self,
                            *allowed_statuses: LifecycleStatus,
                            new_status: LifecycleStatus):
        self.ensure_status(*allowed_statuses)

        previous_status = self.general_state.bot_status
        self.general_state.bot_status = new_status

        logger.info(
            "Bot lifecycle status changed "
            "bot_id=%s previous_status=%s new_status=%s",
            self.general_state.bot_id,
            previous_status.value,
            new_status.value,
        )
        
    def run(self):
        self.change_status(
            LifecycleStatus.STARTED,
            new_status=LifecycleStatus.RUNNING
        )
