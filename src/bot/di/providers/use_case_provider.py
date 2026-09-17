from dishka import Provider, Scope, provide

from bot.use_cases.lifecycle.start_bot_uc import StartBotUC
from bot.use_cases.state.trading_state.add_tracking_market_uc import AddTrackingMarketUC

class LifecycleUCProvider(Provider):
    scope = Scope.APP
    
    start_bot_uc = provide(StartBotUC)
    
    add_tracking_market_uc = provide(AddTrackingMarketUC)