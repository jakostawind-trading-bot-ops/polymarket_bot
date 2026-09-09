from dishka import provide, Provider, Scope

from bot.nats.decoder import CommandDecoder
from bot.commands.dispatcher import CommandDispatcher
from bot.nats.routes.lifecycle import LIFECYCLE_ROUTES
from bot.commands.lifecycle_cmd import RunBotCommand, RunBotHandler

class CommandProvider(Provider):
    scope = Scope.APP

    run_bot_handler = provide(RunBotHandler)

    @provide
    def provide_decoder(self) -> CommandDecoder:
        return CommandDecoder(
            routes=LIFECYCLE_ROUTES,
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