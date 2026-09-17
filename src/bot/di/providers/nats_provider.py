import logging
from collections.abc import AsyncIterator

import nats
from dishka import Provider, Scope, provide
from nats.aio.client import Client
from nats.js.client import JetStreamContext

from bot.bootstrap import BootstrapSettings
from bot.commands.dispatcher import CommandDispatcher
from bot.transport.nats.decoder import CommandDecoder
from bot.transport.nats.publisher import NatsPublisher
from bot.transport.nats.subcriber import NatsSubscriber
from bot.ports.command_subscriber import CommandSubscriber
from bot.ports.event_publisher import EventPublisher
from bot.state.general_state import GeneralState

CONTROL_TO_BOT_COMMANDS = "CONTROL_TO_BOT_COMMANDS"
BOT_TO_CONTROL_EVENTS = "BOT_TO_CONTROL_EVENTS"


logger = logging.getLogger(__name__)


class NatsProvider(Provider):
    scope = Scope.APP

    @provide
    async def provide_nats_client(
        self,
        bootstrap_settings: BootstrapSettings,
    ) -> AsyncIterator[Client]:
        logger.info("Connecting to NATS")

        try:
            client = await nats.connect(
                bootstrap_settings.nats_url,
            )
        except Exception:
            logger.exception("Failed to connect to NATS")
            raise

        logger.info("NATS connection established")

        try:
            yield client
        finally:
            logger.info("Closing NATS connection")
            await client.close()
            logger.info("NATS connection closed")

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
        publisher: EventPublisher,
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
            publisher=publisher,
        )
        
        await subscriber.start()

        try:
            yield subscriber
        finally:
            await subscriber.close()
            
