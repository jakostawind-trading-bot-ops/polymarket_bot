from dishka import provide, Provider, Scope

from bot.commands.dispatcher import CommandDispatcher
from bot.commands.lifecycle_cmds.run_bot_cmd import RunBotCommand, RunBotHandler
from bot.nats.decoder import CommandDecoder
from bot.nats.routes.registry import COMMAND_ROUTES

class CommandProvider(Provider):
    scope = Scope.APP

    run_bot_handler = provide(RunBotHandler)

    @provide
    def provide_decoder(self) -> CommandDecoder:
        return CommandDecoder(
            routes=COMMAND_ROUTES,
        )

    @provide
    def provide_dispatcher(
        self,
        run_bot_handler: RunBotHandler,
    ) -> CommandDispatcher:
        return CommandDispatcher(
            handlers={
                RunBotCommand: run_bot_handler,
            },
        )
