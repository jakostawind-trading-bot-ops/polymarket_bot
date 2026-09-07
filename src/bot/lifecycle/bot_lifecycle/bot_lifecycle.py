from enum import StrEnum

class LifecycleStatuses(StrEnum):
    STARTED = "started" # процесс запущен, бот ожидвает инструкций или прямого запуска от адмники
    

class BotLifecycle():
    def __init__(self):
        self.statuses = LifecycleStatuses
        
    async def start():
        pass