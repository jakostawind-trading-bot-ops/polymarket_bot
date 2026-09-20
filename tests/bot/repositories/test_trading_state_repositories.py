import asyncio
from dataclasses import replace

import pytest

from bot.entities.market_info import MarketInfo
from bot.repositories.trading_state.memory import trading_state_repo_mem
from bot.repositories.trading_state.memory.market_info_repo_mem import MarketInfoRepoMem
from bot.repositories.trading_state.memory.market_state_repo_mem import MarketStateRepoMem
from bot.repositories.trading_state.memory.trading_state_repo_mem import TradingStateRepoMem
from bot.state.trading_state import MarketState, TradingState


@pytest.fixture
def market_info():
    return MarketInfo(
        market_id=123,
        question="Будет ли событие?",
        asset_ids=(2**255 + 1, 2**256 - 1),
        condition_id="0x" + "a" * 64,
        slug="example-market",
        game_start_time="2026-09-20T12:00:00Z",
        end_date="2026-09-21T12:00:00Z",
    )


@pytest.fixture
def trading_state():
    return TradingState()


@pytest.fixture
def trading_repo(trading_state):
    return TradingStateRepoMem(trading_state)


def test_track_market_preserves_metadata_and_connects_repositories(
    trading_repo, trading_state, market_info,
):
    expected = replace(market_info)
    asyncio.run(trading_repo.track_market(market_info))
    child = asyncio.run(trading_repo.get_market_state_repo(market_info.market_id))

    assert set(trading_state.tracking_markets) == {market_info.market_id}
    state = trading_state.tracking_markets[market_info.market_id]
    assert state.market_info == expected
    assert child.market_state is state
    assert child.market_info_repo.market_state is state
    assert asyncio.run(
        trading_repo.get_market_state_repo(market_info.market_id)
    ) is child


def test_track_market_accepts_absent_optional_metadata(
    trading_repo, trading_state,
):
    info = MarketInfo(market_id=1, question="", asset_ids=(10, 20))

    asyncio.run(trading_repo.track_market(info))

    assert trading_state.tracking_markets[1].market_info == info


def test_duplicate_market_does_not_replace_existing_state(
    trading_repo, trading_state, market_info,
):
    expected = replace(market_info)
    asyncio.run(trading_repo.track_market(market_info))
    state = trading_state.tracking_markets[market_info.market_id]
    child = asyncio.run(trading_repo.get_market_state_repo(market_info.market_id))
    duplicate = replace(market_info, question="Другая информация", asset_ids=(1, 2))

    with pytest.raises(ValueError, match=str(market_info.market_id)):
        asyncio.run(trading_repo.track_market(duplicate))

    assert set(trading_state.tracking_markets) == {market_info.market_id}
    assert trading_state.tracking_markets[market_info.market_id] is state
    assert state.market_info == expected
    assert asyncio.run(
        trading_repo.get_market_state_repo(market_info.market_id)
    ) is child


def test_missing_market_lookup_does_not_change_state(
    trading_repo, trading_state, market_info,
):
    asyncio.run(trading_repo.track_market(market_info))
    before = dict(trading_state.tracking_markets)

    with pytest.raises(KeyError) as caught:
        asyncio.run(trading_repo.get_market_state_repo(999))

    assert caught.value.args == (999,)
    assert trading_state.tracking_markets == before
    child = asyncio.run(trading_repo.get_market_state_repo(market_info.market_id))
    assert child.market_state is before[market_info.market_id]


def test_separate_trading_states_are_isolated(market_info):
    first_state, second_state = TradingState(), TradingState()
    first, second = TradingStateRepoMem(first_state), TradingStateRepoMem(second_state)
    asyncio.run(first.track_market(market_info))

    assert second_state.tracking_markets == {}
    with pytest.raises(KeyError):
        asyncio.run(second.get_market_state_repo(market_info.market_id))

    other = replace(market_info, question="Другой экземпляр")
    asyncio.run(second.track_market(other))
    assert first_state.tracking_markets[market_info.market_id].market_info == market_info
    assert second_state.tracking_markets[market_info.market_id].market_info == other


def test_updating_one_market_does_not_change_another(
    trading_repo, trading_state, market_info,
):
    other = replace(market_info, market_id=456, question="Другой рынок")
    asyncio.run(trading_repo.track_market(market_info))
    asyncio.run(trading_repo.track_market(other))
    first = asyncio.run(trading_repo.get_market_state_repo(market_info.market_id))
    second = asyncio.run(trading_repo.get_market_state_repo(other.market_id))
    updated = replace(market_info, question="Новые данные", asset_ids=(30, 40))

    asyncio.run(first.market_info_repo.add_market(updated))

    assert trading_state.tracking_markets[market_info.market_id].market_info == updated
    assert trading_state.tracking_markets[other.market_id].market_info == other
    assert first.market_state is not second.market_state


def test_concurrent_duplicate_tracking_has_one_winner(
    trading_repo, trading_state, market_info,
):
    candidates = [
        replace(market_info, question=f"Версия {index}")
        for index in range(8)
    ]

    async def run():
        return await asyncio.gather(
            *(trading_repo.track_market(info) for info in candidates),
            return_exceptions=True,
        )

    results = asyncio.run(run())
    winners = [index for index, result in enumerate(results) if result is None]
    assert len(winners) == 1
    assert sum(isinstance(result, ValueError) for result in results) == 7
    winner = candidates[winners[0]]
    assert set(trading_state.tracking_markets) == {market_info.market_id}
    assert trading_state.tracking_markets[market_info.market_id].market_info == winner
    child = asyncio.run(trading_repo.get_market_state_repo(market_info.market_id))
    assert child.market_state is trading_state.tracking_markets[market_info.market_id]


def test_concurrent_distinct_markets_remain_accessible(
    trading_repo, trading_state, market_info,
):
    markets = [replace(market_info, market_id=index) for index in range(1, 9)]

    async def run():
        await asyncio.gather(*(trading_repo.track_market(info) for info in markets))
        return await asyncio.gather(
            *(trading_repo.get_market_state_repo(info.market_id) for info in markets)
        )

    children = asyncio.run(run())

    assert set(trading_state.tracking_markets) == {info.market_id for info in markets}
    for info, child in zip(markets, children, strict=True):
        assert child.market_state is trading_state.tracking_markets[info.market_id]
        assert child.market_state.market_info == info


def test_child_creation_failure_leaves_state_unchanged_and_allows_retry(
    trading_repo, trading_state, market_info, monkeypatch,
):
    asyncio.run(trading_repo.track_market(market_info))
    original = asyncio.run(trading_repo.get_market_state_repo(market_info.market_id))
    another = replace(market_info, market_id=456)
    error = RuntimeError("Cannot initialize market repository")

    def fail_to_create(*args, **kwargs):
        raise error

    with monkeypatch.context() as patch:
        patch.setattr(trading_state_repo_mem, "MarketStateRepoMem", fail_to_create)
        with pytest.raises(RuntimeError) as caught:
            asyncio.run(trading_repo.track_market(another))

    assert caught.value is error
    assert set(trading_state.tracking_markets) == {market_info.market_id}
    assert trading_state.tracking_markets[market_info.market_id] is original.market_state
    assert original.market_state.market_info == market_info
    assert asyncio.run(
        trading_repo.get_market_state_repo(market_info.market_id)
    ) is original
    with pytest.raises(KeyError):
        asyncio.run(trading_repo.get_market_state_repo(another.market_id))

    asyncio.run(trading_repo.track_market(another))
    child = asyncio.run(trading_repo.get_market_state_repo(another.market_id))
    assert child.market_state is trading_state.tracking_markets[another.market_id]
    assert child.market_state.market_info == another


@pytest.mark.parametrize("wrapped", [False, True], ids=["info-repo", "state-repo"])
def test_market_info_update_reaches_original_state(market_info, wrapped):
    state = MarketState(market_info)
    repository = MarketStateRepoMem(state) if wrapped else MarketInfoRepoMem(state)
    info_repo = repository.market_info_repo if wrapped else repository
    updated = replace(
        market_info,
        question="Новый вопрос",
        asset_ids=(30, 40),
        condition_id=None,
        slug=None,
        game_start_time=None,
        end_date=None,
    )

    asyncio.run(info_repo.add_market(updated))

    assert repository.market_state is state
    assert state.market_info == updated


def test_existing_runtime_state_is_accessible_when_repository_is_created(market_info):
    state = MarketState(market_info)
    trading_state = TradingState(tracking_markets={market_info.market_id: state})
    repository = TradingStateRepoMem(trading_state)

    child = asyncio.run(repository.get_market_state_repo(market_info.market_id))

    assert child.market_state is state
    updated = replace(market_info, question="Обновлённый вопрос")
    asyncio.run(child.market_info_repo.add_market(updated))
    assert trading_state.tracking_markets[market_info.market_id] is state
    assert state.market_info == updated


def test_metadata_update_cannot_replace_market_identity(
    trading_repo, trading_state, market_info,
):
    asyncio.run(trading_repo.track_market(market_info))
    child = asyncio.run(trading_repo.get_market_state_repo(market_info.market_id))
    wrong_market = replace(market_info, market_id=456)

    with pytest.raises(ValueError):
        asyncio.run(child.market_info_repo.add_market(wrong_market))

    assert set(trading_state.tracking_markets) == {market_info.market_id}
    assert child.market_state is trading_state.tracking_markets[market_info.market_id]
    assert child.market_state.market_info == market_info
    with pytest.raises(KeyError):
        asyncio.run(trading_repo.get_market_state_repo(wrong_market.market_id))


@pytest.mark.parametrize("replace_metadata", [False, True], ids=["track", "update"])
def test_changing_input_id_does_not_corrupt_market_index(
    trading_repo, trading_state, market_info, replace_metadata,
):
    market_id = market_info.market_id
    asyncio.run(trading_repo.track_market(market_info))
    child = asyncio.run(trading_repo.get_market_state_repo(market_id))
    source = market_info
    if replace_metadata:
        source = replace(market_info, question="Обновление")
        asyncio.run(child.market_info_repo.add_market(source))

    try:
        source.market_id = 456
    except (AttributeError, ValueError):
        pass  # Rejecting an identity change also preserves the invariant.

    assert set(trading_state.tracking_markets) == {market_id}
    assert trading_state.tracking_markets[market_id].market_info.market_id == market_id
    assert asyncio.run(trading_repo.get_market_state_repo(market_id)) is child
    with pytest.raises(KeyError):
        asyncio.run(trading_repo.get_market_state_repo(456))
