from dishka import Provider, Scope, provide

from bot.use_cases import (
                                    StartBotUC, 
                                    RunBotUc
                                    )
from bot.use_cases.state.trading_state.add_tracking_market_uc import AddTrackingMarketUC

class LifecycleUCProvider(Provider):
    scope = Scope.APP
    
    start_bot_uc = provide(StartBotUC)
    run_bot_uc = provide(RunBotUc)
    
    
    
class TradingStateUCProvider(Provider):
    scope = Scope.APP
    
    add_tracking_market_uc = provide(AddTrackingMarketUC)