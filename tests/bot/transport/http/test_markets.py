import asyncio

import httpx
import pytest
from pydantic import ValidationError

from bot.entities.market import Market
from bot.transport.http.httpx_client import HttpxClient
from bot.transport.http.polymarket_api.markets import get_market_by_id


@pytest.fixture
def market_payload():
    return {
        "id": "123",
        "conditionId": "0x" + "a" * 64,
        "slug": "example-market",
        "question": "Will the example happen?",
        "clobTokenIds": '["123456789012345678901234567890", "456"]',
        "gameStartTime": "2026-09-17T12:00:00Z",
        "endDate": "2026-09-18T12:00:00Z",
        "volume": "1000",
        "events": [{"id": "789"}],
    }


def fetch_market(payload: object, status_code: int = 200) -> Market:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert str(request.url) == "https://gamma-api.polymarket.com/markets/123"
        return httpx.Response(status_code, json=payload)

    async def run() -> Market:
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(handler),
        ) as client:
            return await get_market_by_id(HttpxClient(client), 123)

    return asyncio.run(run())


def test_returns_market_from_gamma_response(market_payload):
    market = fetch_market(market_payload)

    assert market == Market(
        market_id=123,
       condition_id="0x" + "a" * 64,
        slug="example-market",
        question="Will the example happen?",
        asset_ids=(123456789012345678901234567890, 456),
        game_start_time="2026-09-17T12:00:00Z",
        end_date="2026-09-18T12:00:00Z",
    )


@pytest.mark.parametrize("missing", [True, False])
def test_accepts_missing_or_null_optional_fields(market_payload, missing):
    for field in ("slug", "question", "gameStartTime", "endDate"):
        if missing:
            market_payload.pop(field)
        else:
            market_payload[field] = None

    market = fetch_market(market_payload)

    assert market.slug is None
    assert market.question is None
    assert market.game_start_time is None
    assert market.end_date is None


@pytest.mark.parametrize("status_code", [302, 404, 429, 500])
def test_rejects_http_errors_before_parsing_market(status_code):
    with pytest.raises(RuntimeError, match=f"HTTP {status_code}"):
        fetch_market({"error": "Request failed"}, status_code)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("id", "invalid"),
        ("conditionId", None),
        ("clobTokenIds", None),
        ("clobTokenIds", "invalid-json"),
        ("clobTokenIds", '["invalid-token-id"]'),
    ],
)
def test_rejects_invalid_required_fields(market_payload, field, value):
    market_payload[field] = value

    with pytest.raises(ValidationError):
        fetch_market(market_payload)


def test_rejects_missing_required_field(market_payload):
    market_payload.pop("conditionId")

    with pytest.raises(ValidationError):
        fetch_market(market_payload)