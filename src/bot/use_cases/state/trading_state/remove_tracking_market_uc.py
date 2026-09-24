import logging

from bot.repositories.trading_state.abstract.trading_state_repo_abc import TradingStateRepoABC
from bot.ports.event_publisher import EventPublisher
from bot.events.trading_state_ev import TrackingMarketRemovedEvent

logger = logging.getLogger(__name__)

class RemoveTrackingMarketUC():
    def __init__(
        self,
        trading_state_repo: TradingStateRepoABC,
        publisher_port: EventPublisher
    ):
        self.trading_state_repo = trading_state_repo
        self.publisher = publisher_port
        
    async def execute(self, market_id: int):
        logger.info("Прекращение отслеживания рынка: market_id=%s", market_id)
        
        try:
            stage = "remove_from_state"
            await self.trading_state_repo.untrack_market(market_id=market_id)
            logger.info("Репозиторий удалил маркет из TradingState: market_id=%s", market_id)
            
            stage = "publish_event"
            await self.publisher.publish_event(
                TrackingMarketRemovedEvent(
                    market_id=market_id
                )
            )
            logger.info("Опубликован event удаления рынка: market_id=%s", market_id)
            
        except Exception:
            logger.exception(
                "Не удалось прекратить отслеживать рынок: market_id=%s stage=%s",
                market_id,
                stage,
            )
            raise