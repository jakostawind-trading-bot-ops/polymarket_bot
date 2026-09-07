from dishka import Provider, Scope, from_context

from bot.bootstrap import BootstrapSettings

class BootstrapSettingsProvider(Provider):
    scope = Scope.APP
    
    bootstrap_settings = from_context(
        provides=BootstrapSettings
    )