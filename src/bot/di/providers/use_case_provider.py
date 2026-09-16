from dishka import Provider, Scope, provide

from bot.use_cases.lifecycle.start_bot_uc import StartBotUC

class LifecycleUCProvider(Provider):
    scope = Scope.APP
    
    start_bot_uc = provide(StartBotUC)
    # run_bot_uc = provide(RunBotUC)