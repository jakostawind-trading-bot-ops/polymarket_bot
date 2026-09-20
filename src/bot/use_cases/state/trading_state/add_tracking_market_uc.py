import logging

from bot.repositories.trading_state.abstract.trading_state_repo_abc import TradingStateRepoABC
from bot.entities.market_info import MarketInfo
from bot.ports.event_publisher import EventPublisher
from bot.ports.http_client import HttpClient
from bot.events.trading_state_ev import TrackingMarketAddedEvent

from polymarket_sdk.http import get_market_by_id 

logger = logging.getLogger(__name__)

class AddTrackingMarketUC():
    def __init__(
        self,
        trading_state_repo: TradingStateRepoABC,
        publisher_port: EventPublisher,
        http_client_port: HttpClient
    ):
        self.trading_state_repo = trading_state_repo
        self.publisher = publisher_port
        self.http_client = http_client_port
        
    async def execute(self, market_id: int):
        logger.info("Добавление рынка для отслеживания: market_id=%s", market_id)
        stage = "fetch_market"

        try:
            sdk_market = await get_market_by_id(
                http_client=self.http_client,
                market_id=market_id,
            )
            market_info = MarketInfo(**sdk_market.model_dump())
            logger.info("Данные рынка получены: market_id=%s", market_id)

            stage = "trading_stage_add"
            await self.trading_state_repo.track_market(market_info=market_info)
            logger.info("Добавление в trading_stage завершено: market_id=%s", market_id)

            stage = "publish_event"
            await self.publisher.publish_event(
                TrackingMarketAddedEvent(market_info=market_info)
            )
            logger.info("Опубликован event добавления рынка: market_id=%s", market_id)
        except Exception:
            logger.exception(
                "Не удалось добавить рынок для отслеживания: market_id=%s stage=%s",
                market_id,
                stage,
            )
            raise
        
        
