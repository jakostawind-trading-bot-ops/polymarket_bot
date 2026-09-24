from dishka import provide, Provider, Scope

from bot.commands.dispatcher import CommandDispatcher
from bot.transport.nats.decoder import CommandDecoder
from bot.transport.nats.command_routes.registry import COMMAND_ROUTES

from bot.commands import (
    RunBotCommand, RunBotHandler,
    AddTrackingMarketCommand, AddTrackingMarketHandler,
    RemoveTrackingMarketCommand, RemoveTrackingMarketHandler
)


class CommandProvider(Provider):
    scope = Scope.APP

    # lifecycle
    run_bot_handler = provide(RunBotHandler)
    
    # acccont state
    # add_account_state_handler = provide(AddAccountStateHandler)
    
    # trading_state
    add_tracking_market_handler = provide(AddTrackingMarketHandler)
    remove_tracking_market_handler = provide(RemoveTrackingMarketHandler)

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
        # add_account_state_handler: AddAccountStateHandler,
        
        # trading_state
        add_tracking_market_handler: AddTrackingMarketHandler,
        remove_tracking_market_handler: RemoveTrackingMarketHandler
    ) -> CommandDispatcher:
        return CommandDispatcher(
            handlers={
                # lifecycle
                RunBotCommand: run_bot_handler,
                
                # state
                # AddAccountStateCommand: add_account_state_handler,
                
                # trading_state
                AddTrackingMarketCommand: add_tracking_market_handler,
                RemoveTrackingMarketCommand: remove_tracking_market_handler
            },
        )
