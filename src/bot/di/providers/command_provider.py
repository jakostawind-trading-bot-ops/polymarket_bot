from dishka import provide, Provider, Scope

from bot.commands.dispatcher import CommandDispatcher
from bot.nats.decoder import CommandDecoder
from bot.nats.command_routes.registry import COMMAND_ROUTES

from bot.commands.lifecycle_cmds.run_bot_cmd import RunBotCommand, RunBotHandler
from bot.commands.state_cmds.add_polymarket_state_cmd import AddPolymarketStateCommand, AddPolymarketStateHandler


class CommandProvider(Provider):
    scope = Scope.APP

    # lifecycle
    run_bot_handler = provide(RunBotHandler)
    
    # state
    add_polymarket_state_handler = provide(AddPolymarketStateHandler)

    @provide
    def provide_decoder(self) -> CommandDecoder:
        return CommandDecoder(
            routes=COMMAND_ROUTES,
        )

    @provide
    def provide_dispatcher(
        self,
        # lifecycle
        run_bot_handler: RunBotHandler,
        
        # state
        add_polymarket_state_handler: AddPolymarketStateHandler
    ) -> CommandDispatcher:
        return CommandDispatcher(
            handlers={
                # lifecycle
                RunBotCommand: run_bot_handler,
                
                # state
                AddPolymarketStateCommand: add_polymarket_state_handler
            },
        )
