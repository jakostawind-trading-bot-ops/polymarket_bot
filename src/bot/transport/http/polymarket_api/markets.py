from pydantic import BaseModel, Field, Json

from bot.ports.http_client import HttpClient
from bot.entities.market import Market

from bot.transport.http.polymarket_api.urls import GET_MARKET_BY_ID

class PolymarketMarket(BaseModel):
    market_id: int = Field(alias="id")
    condition_id: str = Field(alias="conditionId")
    asset_ids: Json[tuple[int, ...]] = Field(alias="clobTokenIds")
    slug: str | None = None
    question: str | None = None
    game_start_time: str | None = Field(default=None, alias="gameStartTime")
    end_date: str | None = Field(default=None, alias="endDate")
    
async def get_market_by_id(
    http_client_port: HttpClient,
    market_id: int
) -> Market:
    response = await http_client_port.request(
        "GET",
        GET_MARKET_BY_ID.format(id = market_id),
    )
    
    if response.status_code != 200:
        raise RuntimeError(
            f"Failed to fetch market {market_id}: HTTP {response.status_code}"
        )
    
    market = PolymarketMarket.model_validate(response.json())
    return Market(**market.model_dump())