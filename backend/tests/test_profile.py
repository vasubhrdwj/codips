"""
Unit tests for GET /api/v1/profile/{handle}

Uses httpx's MockTransport to intercept outbound requests so the tests
never hit the real Codeforces API.
"""
import json
import pytest
import httpx
from fastapi.testclient import TestClient

from app.main import app
from app.api.v1 import profile as profile_module

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

CF_SUCCESS = {
    "status": "OK",
    "result": [
        {
            "handle": "tourist",
            "rating": 3755,
            "maxRating": 4009,
            "rank": "legendary grandmaster",
            "maxRank": "tourist",
            "contribution": 75,
            "friendOfCount": 88047,
        }
    ],
}

CF_FAILED = {
    "status": "FAILED",
    "comment": "handles: User with handle tourist not found",
}

CF_EMPTY_RESULT = {
    "status": "OK",
    "result": [],
}


def make_mock_transport(response_body: dict, status_code: int = 200):
    """Return an httpx MockTransport that always replies with the given body."""

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=status_code,
            headers={"Content-Type": "application/json"},
            content=json.dumps(response_body).encode(),
        )

    return httpx.MockTransport(handler)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def clear_cache():
    """Wipe the in-memory cache before every test for isolation."""
    profile_module.profile_cache.clear()
    yield
    profile_module.profile_cache.clear()


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestGetProfile:

    def test_success_returns_cleaned_profile(self, client, monkeypatch):
        """Happy path: Codeforces returns OK → we get the cleaned fields."""
        OriginalAsyncClient = httpx.AsyncClient
        monkeypatch.setattr(
            httpx,
            "AsyncClient",
            lambda **_: OriginalAsyncClient(transport=make_mock_transport(CF_SUCCESS)),
        )
        resp = client.get("/api/v1/profile/tourist")

        assert resp.status_code == 200
        data = resp.json()
        assert data["handle"] == "tourist"
        assert data["rating"] == 3755
        assert data["maxRating"] == 4009
        assert data["rank"] == "legendary grandmaster"
        assert data["maxRank"] == "tourist"
        assert data["contribution"] == 75
        assert data["friendOfCount"] == 88047

    def test_codeforces_failed_status_returns_400(self, client, monkeypatch):
        """When Codeforces returns status=FAILED the endpoint raises HTTP 400."""
        OriginalAsyncClient = httpx.AsyncClient
        monkeypatch.setattr(
            httpx,
            "AsyncClient",
            lambda **_: OriginalAsyncClient(transport=make_mock_transport(CF_FAILED)),
        )
        resp = client.get("/api/v1/profile/tourist")

        assert resp.status_code == 400
        assert "not found" in resp.json()["detail"].lower()

    def test_empty_result_returns_404(self, client, monkeypatch):
        """When result list is empty the endpoint raises HTTP 404."""
        OriginalAsyncClient = httpx.AsyncClient
        monkeypatch.setattr(
            httpx,
            "AsyncClient",
            lambda **_: OriginalAsyncClient(transport=make_mock_transport(CF_EMPTY_RESULT)),
        )
        resp = client.get("/api/v1/profile/ghost")

        assert resp.status_code == 404

    def test_network_error_returns_503(self, client, monkeypatch):
        """When httpx raises a RequestError the endpoint raises HTTP 503."""
        def raise_network_error(request: httpx.Request) -> httpx.Response:
            raise httpx.ConnectError("connection refused", request=request)

        OriginalAsyncClient = httpx.AsyncClient
        monkeypatch.setattr(
            httpx,
            "AsyncClient",
            lambda **_: OriginalAsyncClient(transport=httpx.MockTransport(raise_network_error)),
        )
        resp = client.get("/api/v1/profile/tourist")

        assert resp.status_code == 503

    def test_cached_response_not_refetched(self, client, monkeypatch):
        """Second request for same handle uses cache; external API called only once."""
        call_count = {"n": 0}

        def counting_handler(request: httpx.Request) -> httpx.Response:
            call_count["n"] += 1
            return httpx.Response(
                200,
                headers={"Content-Type": "application/json"},
                content=json.dumps(CF_SUCCESS).encode(),
            )

        OriginalAsyncClient = httpx.AsyncClient
        monkeypatch.setattr(
            httpx,
            "AsyncClient",
            lambda **_: OriginalAsyncClient(transport=httpx.MockTransport(counting_handler)),
        )

        client.get("/api/v1/profile/tourist")
        client.get("/api/v1/profile/tourist")

        assert call_count["n"] == 1, "Codeforces API should only be called once due to caching"

    def test_optional_fields_can_be_none(self, client, monkeypatch):
        """Unrated users (no rating/rank) produce None for optional fields."""
        unrated_response = {
            "status": "OK",
            "result": [
                {
                    "handle": "newbie_user",
                    "contribution": 0,
                    "friendOfCount": 1,
                    # rating, maxRating, rank, maxRank intentionally absent
                }
            ],
        }
        OriginalAsyncClient = httpx.AsyncClient
        monkeypatch.setattr(
            httpx,
            "AsyncClient",
            lambda **_: OriginalAsyncClient(transport=make_mock_transport(unrated_response)),
        )
        resp = client.get("/api/v1/profile/newbie_user")

        assert resp.status_code == 200
        data = resp.json()
        assert data["rating"] is None
        assert data["rank"] is None
