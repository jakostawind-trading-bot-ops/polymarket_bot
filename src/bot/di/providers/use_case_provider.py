from dishka import Provider, Scope, provide

from bot.use_cases.lifecycle_uc import StartBotUC

class LifecycleUCProvider(Provider):
    scope = Scope.APP
    
    start_bot_uc = provide(StartBotUC)