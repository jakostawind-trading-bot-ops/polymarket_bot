from collections.abc import AsyncIterator

import nats
from dishka import Provider, Scope, provide
from nats.aio.client import Client
from nats.js.client import JetStreamContext

from bot.bootstrap import BootstrapSettings
from bot.commands.dispatcher import CommandDispatcher
from bot.nats.decoder import CommandDecoder
from bot.nats.publisher import NatsPublisher
from bot.nats.subcriber import NatsSubscriber
from bot.nats.routes.lifecycle import LIFECYCLE_ROUTES
from bot.ports.command_subscriber import CommandSubscriber
from bot.ports.event_publisher import EventPublisher
from bot.state.general_state import GeneralState


class NatsProvider(Provider):
    scope = Scope.APP

    @provide
    async def provide_nats_client(
        self,
        bootstrap_settings: BootstrapSettings,
    ) -> AsyncIterator[Client]:
        client = await nats.connect(
            bootstrap_settings.nats_url,
        )

        try:
            yield client
        finally:
            await client.close()

    @provide
    def provide_jetstream(
        self,
        nats_client: Client,
    ) -> JetStreamContext:
        return nats_client.jetstream()

    nats_publisher = provide(
        NatsPublisher,
        provides=EventPublisher,
    )

    @provide
    async def provide_nats_subscriber(
        self,
        jetstream: JetStreamContext,
        general_state: GeneralState,
        decoder: CommandDecoder,
        dispatcher: CommandDispatcher,
    ) -> AsyncIterator[CommandSubscriber]:
        subscriber = NatsSubscriber(
            jetstream=jetstream,
            subject=f"bot.{general_state.bot_id}.command.*",
            decoder=decoder,
            dispatcher=dispatcher,
        )
        
        await subscriber.start()

        try:
            yield subscriber
        finally:
            await subscriber.close()

        
    @provide
    def provide_command_decoder(self) -> CommandDecoder:
            return CommandDecoder(
                routes=LIFECYCLE_ROUTES,
            )
            


