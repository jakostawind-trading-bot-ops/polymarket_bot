from dataclasses import dataclass


@dataclass
class MarketInfo():
    market_id: int
    question: str
    asset_ids: tuple[int, ...]
    condition_id: str | None = None
    slug: str | None = None
    game_start_time: str | None = None
    end_date: str | None = None