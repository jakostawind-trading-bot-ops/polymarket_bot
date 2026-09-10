from dataclasses import dataclass
from pydantic import BaseModel, ConfigDict

from bot.commands.command import Command, CommandHandler

class RunBotSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

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