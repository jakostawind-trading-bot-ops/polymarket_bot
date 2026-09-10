from dataclasses import dataclass
from pydantic import BaseModel

from bot.commands.command import Command, CommandHandler

class RunBotSchema(BaseModel):
    ...

@dataclass
class RunBotCommand(Command):
    ... 
    
class RunBotHandler(CommandHandler):
    async def handle(
        self,
        command: RunBotCommand,
    ) -> None:
        print(
            f"RunBotHandler вызван, trace_id={command.trace_id}"
        )