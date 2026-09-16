import logging

from bot.repositories.abstract.tracking_markets import TrackingMarketsRepoABC
from bot.state.trading_state import TradingState
from bot.ports.event_publisher import EventPublisher
from bot.events.trading_state_ev import MarketAddedInTrackingMarketsEvent

logger = logging.getLogger(__name__)

class AddTrackingMarketUC():
    def __init__(
        self,
        tracking_markets_repo_abc: TrackingMarketsRepoABC,
        trading_state: TradingState,
        publisher: EventPublisher
    ):
        self.tracking_markets_repo_abc = tracking_markets_repo_abc
        self.trading_state = trading_state
        self.publisher = publisher
        
    async def execute(self):
        market = "" # запрос в полимаркет на получание данных маркета
        
        await self.tracking_markets_repo_abc.add()
        
        await self.publisher.publish_event(MarketAddedInTrackingMarketsEvent(
            # тут типа публикуется ивент с данными маркета
        ))
        
        