from dishka import provide, Provider, Scope

from bot.commands.dispatcher import CommandDispatcher
from bot.transport.nats.decoder import CommandDecoder
from bot.transport.nats.command_routes.registry import COMMAND_ROUTES

from bot.commands.lifecycle_cmds.run_bot_cmd import RunBotCommand, RunBotHandler
from bot.commands.state_cmds.account_state.add_account_state_cmd import AddAccountStateCommand, AddAccountStateHandler
from bot.commands.state_cmds.trading_state.add_tracking_market_cmd import AddTrackingMarketCommand, AddTrackingMarketHandle


class CommandProvider(Provider):
    scope = Scope.APP

    # lifecycle
    run_bot_handler = provide(RunBotHandler)
    
    # acccont state
    add_account_state_handler = provide(AddAccountStateHandler)
    
    # trading_state
    add_tracking_market_handler = provide(AddTrackingMarketHandle)

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
        
        # account state
        add_account_state_handler: AddAccountStateHandler,
        
        # trading_state
        add_tracking_market_handler: AddTrackingMarketHandle
    ) -> CommandDispatcher:
        return CommandDispatcher(
            handlers={
                # lifecycle
                RunBotCommand: run_bot_handler,
                
                # state
                AddAccountStateCommand: add_account_state_handler,
                
                # trading_state
                AddTrackingMarketCommand: add_tracking_market_handler
            },
        )
