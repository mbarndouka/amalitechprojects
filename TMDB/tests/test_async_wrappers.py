import pandas as pd
import pytest
import httpx

import api.api as api_module
import index as index_module
from api.api import TMDB


def _build_client(monkeypatch):
    monkeypatch.setattr(api_module, "api_key", "test-key")
    monkeypatch.setattr(api_module, "base_url", "https://example.test")
    return TMDB()


def test_get_movies_batch_without_running_loop(monkeypatch):
    """"
    This test verifies that the synchronous wrapper around the asynchronous batch fetching method works.
    The function `get_movies_batch` is called outside of an async context, so it should handle the event loop itself.

    """
    client = _build_client(monkeypatch)

    async def fake_batch(self, movie_ids, max_concurrent=10):
        return [{"id": movie_id} for movie_id in movie_ids]

    monkeypatch.setattr(TMDB, "get_movies_batch_async", fake_batch)

    result = client.get_movies_batch([1, 2, 3], max_concurrent=2)
    assert result == [{"id": 1}, {"id": 2}, {"id": 3}]


@pytest.mark.asyncio
async def test_get_movie_with_credits_uses_append_to_response(monkeypatch):
    """"
    This test verifies that when fetching a movie with credits, the append_to_response parameter is set correctly.
    """
    client = _build_client(monkeypatch)
    calls = []

    class DummyAsyncClient:
        async def get(self, url, params=None):
            calls.append((url, params))
            req = httpx.Request("GET", url, params=params)
            payload = {
                "id": 299534,
                "title": "Avengers: Endgame",
                "credits": {"cast": [], "crew": []},
            }
            return httpx.Response(200, request=req, json=payload)

    result = await client.get_movie_with_credits_async(DummyAsyncClient(), 299534)

    assert result is not None
    assert result["id"] == 299534
    assert "credits" in result
    assert len(calls) == 1
    _, params = calls[0]
    assert params["append_to_response"] == "credits"


@pytest.mark.asyncio
async def test_get_movies_batch_filters_not_found(monkeypatch):
    """
    This test verifies that movies that are not found are filtered out of the result.
    """
    client = _build_client(monkeypatch)

    async def fake_fetch(self, _client, movie_id):
        if movie_id == 0:
            return None
        return {"id": movie_id, "credits": {"cast": [], "crew": []}}

    monkeypatch.setattr(TMDB, "get_movie_with_credits_async", fake_fetch)

    result = await client.get_movies_batch_async([0, 299534], max_concurrent=2)
    assert result == [{"id": 299534, "credits": {"cast": [], "crew": []}}]


@pytest.mark.asyncio
async def test_get_movies_batch_inside_running_loop(monkeypatch):
    """"
    This test verifies that the synchronous wrapper around the asynchronous batch fetching method works.
    The function `get_movies_batch` is called inside an async context, so it should not handle the event loop itself.
    However, the underlying `get_movies_batch_async` method is mocked to avoid network requests.
    """
    client = _build_client(monkeypatch)

    async def fake_batch(self, movie_ids, max_concurrent=10):
        return [{"id": movie_id, "ok": True} for movie_id in movie_ids]

    monkeypatch.setattr(TMDB, "get_movies_batch_async", fake_batch)

    result = client.get_movies_batch([10, 20], max_concurrent=1)
    assert result == [{"id": 10, "ok": True}, {"id": 20, "ok": True}]


def test_run_pipeline_executes_async_fetch(monkeypatch):
    calls = {
        "fetched": False,
        "cleaned": False,
        "computed": False,
        "plots": 0,
    }

    async def fake_fetch_movie():
        calls["fetched"] = True
        return pd.DataFrame(
            {
                "id": [1],
                "title": ["Movie"],
                "budget_musd": [20.0],
                "revenue_musd": [30.0],
                "vote_count": [100],
                "vote_average": [7.0],
                "popularity": [50.0],
                "genres": ["Action"],
                "belongs_to_collection": [None],
                "release_date": ["2024-01-01"],
            }
        )

    def fake_clean_movies(df):
        calls["cleaned"] = True
        return df

    def fake_compute_profit(df):
        calls["computed"] = True
        out = df.copy()
        out["profit_musd"] = out["revenue_musd"] - out["budget_musd"]
        out["roi"] = out["profit_musd"] / out["budget_musd"]
        return out

    def _fake_plot(_df):
        calls["plots"] += 1

    monkeypatch.setattr(index_module, "fetch_movie", fake_fetch_movie)
    monkeypatch.setattr(index_module, "clean_movies", fake_clean_movies)
    monkeypatch.setattr(index_module, "compute_profit", fake_compute_profit)
    monkeypatch.setattr(index_module, "plot_roi_by_genre", _fake_plot)
    monkeypatch.setattr(index_module, "plot_revenue_vs_budget", _fake_plot)
    monkeypatch.setattr(index_module, "plot_popularity_vs_rating", _fake_plot)
    monkeypatch.setattr(index_module, "plot_yearly_revenue_trends", _fake_plot)
    monkeypatch.setattr(index_module, "plot_franchise_vs_standalone", _fake_plot)

    index_module.run_pipeline()

    assert calls["fetched"] is True
    assert calls["cleaned"] is True
    assert calls["computed"] is True
    assert calls["plots"] == 5
