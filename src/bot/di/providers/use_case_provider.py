from dishka import Provider, Scope, provide

from bot.use_cases import *

class LifecycleUCProvider(Provider):
    scope = Scope.APP
    
    start_bot_uc = provide(StartBotUC)
    run_bot_uc = provide(RunBotUc)
    
    
    
class TradingStateUCProvider(Provider):
    scope = Scope.APP
    
    add_tracking_market_uc = provide(AddTrackingMarketUC)
    remove_tracking_market_uc = provide(RemoveTrackingMarketUC)