import logging

from bot.repositories.abstract.tracking_markets import TrackingMarketsRepoABC
from bot.state.trading_state import TradingState
from bot.ports.event_publisher import EventPublisher
from bot.ports.http_client import HttpClient
from bot.events.trading_state_ev import TrackingMarketAddedEvent
from bot.transport.http.polymarket_api.markets import get_market_by_id

logger = logging.getLogger(__name__)

class AddTrackingMarketUC():
    def __init__(
        self,
        tracking_markets_repo_abc: TrackingMarketsRepoABC,
        trading_state: TradingState,
        publisher_port: EventPublisher,
        http_client_port: HttpClient
    ):
        self.tracking_markets_repo_abc = tracking_markets_repo_abc
        self.trading_state = trading_state
        self.publisher = publisher_port
        self.http_client = http_client_port
        
    async def execute(self, market_id: int):
        logger.info("Добавление рынка для отслеживания: market_id=%s", market_id)
        stage = "fetch_market"

        try:
            market = await get_market_by_id(
                http_client_port=self.http_client,
                market_id=market_id,
            )
            logger.info("Данные рынка получены: market_id=%s", market_id)

            stage = "repository_add"
            await self.tracking_markets_repo_abc.add(market=market)
            logger.info("Добавление в repository завершено: market_id=%s", market_id)

            stage = "publish_event"
            await self.publisher.publish_event(
                TrackingMarketAddedEvent(market=market)
            )
            logger.info("Опубликован event добавления рынка: market_id=%s", market_id)
        except Exception:
            logger.exception(
                "Не удалось добавить рынок для отслеживания: market_id=%s stage=%s",
                market_id,
                stage,
            )
            raise
        
        
