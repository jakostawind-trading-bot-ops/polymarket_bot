from dataclasses import dataclass
from abc import abstractmethod, ABC

@dataclass
class Command():
    trace_id: str

class CommandHandler(ABC):
    @abstractmethod
    async def handle(self, command: Command):
        ...