from dataclasses import dataclass


@dataclass
class Market():
    market_id: int
    condition_id: str
    slug: str
    question: str
    asset_ids: tuple[int, ...]
    game_start_time: str
    end_date: str