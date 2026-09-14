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
from bot.ports.command_subscriber import CommandSubscriber
from bot.ports.event_publisher import EventPublisher
from bot.state.general_state import GeneralState

CONTROL_TO_BOT_COMMANDS = "CONTROL_TO_BOT_COMMANDS"
BOT_TO_CONTROL_EVENTS = "BOT_TO_CONTROL_EVENTS"

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
    
    @provide
    def provide_nats_publisher(
        self,
        jetstream: JetStreamContext,
        general_state: GeneralState
    ) -> EventPublisher:
        return NatsPublisher(
            jetstream = jetstream,
            stream_name = BOT_TO_CONTROL_EVENTS,
            general_state=general_state
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
            stream_name=CONTROL_TO_BOT_COMMANDS,
            subject_prefix=(
                f"control.to.bot.{general_state.bot_id}.command."
            ),
            consumer_name=(
                f"bot_{general_state.bot_id}"
            ),
            decoder=decoder,
            dispatcher=dispatcher,
        )
        
        await subscriber.start()

        try:
            yield subscriber
        finally:
            await subscriber.close()
            

