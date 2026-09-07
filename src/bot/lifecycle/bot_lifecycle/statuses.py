from enum import StrEnum

class LifecycleStatuses(StrEnum):
    STARTED = "started" # бот ожидвает инструкций или прямого запуска от адмники
    RUNNING = "running" # бот торгует 