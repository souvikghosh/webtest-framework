"""Tests for API client module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import timedelta

from webtest_framework.api import (
    APIClient,
    Response,
    assert_status,
    assert_json_contains,
    assert_response_time,
)


class TestResponse:
    def test_ok_for_success_codes(self):
        response = Response(
            status_code=200,
            json_data={"key": "value"},
            text='{"key": "value"}',
            headers={},
            elapsed_ms=100,
        )
        assert response.ok is True

    def test_not_ok_for_error_codes(self):
        response = Response(
            status_code=404,
            json_data=None,
            text="Not Found",
            headers={},
            elapsed_ms=50,
        )
        assert response.ok is False

    def test_json_returns_data(self):
        response = Response(
            status_code=200,
            json_data={"key": "value"},
            text='{"key": "value"}',
            headers={},
            elapsed_ms=100,
        )
        assert response.json() == {"key": "value"}

    def test_json_raises_for_non_json(self):
        response = Response(
            status_code=200,
            json_data=None,
            text="plain text",
            headers={},
            elapsed_ms=100,
        )
        with pytest.raises(ValueError, match="not JSON"):
            response.json()


class TestAPIClient:
    @pytest.fixture
    def client(self):
        return APIClient("https://api.example.com")

    def test_init(self, client):
        assert client.base_url == "https://api.example.com"
        assert client.timeout == 10

    def test_set_header(self, client):
        client.set_header("X-Custom", "value")
        assert client.default_headers["X-Custom"] == "value"

    def test_set_auth_token(self, client):
        client.set_auth_token("my-token")
        assert client.default_headers["Authorization"] == "Bearer my-token"

    @patch("requests.Session.request")
    def test_get(self, mock_request, client):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        mock_response.text = '{"data": "test"}'
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.elapsed = timedelta(milliseconds=50)
        mock_request.return_value = mock_response

        response = client.get("/users")

        assert response.status_code == 200
        assert response.json() == {"data": "test"}
        mock_request.assert_called_once()

    @patch("requests.Session.request")
    def test_post(self, mock_request, client):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": 1}
        mock_response.text = '{"id": 1}'
        mock_response.headers = {}
        mock_response.elapsed = timedelta(milliseconds=100)
        mock_request.return_value = mock_response

        response = client.post("/users", json={"name": "Test"})

        assert response.status_code == 201


class TestAssertions:
    def test_assert_status_passes(self):
        response = Response(200, {}, "", {}, 100)
        assert_status(response, 200)  # Should not raise

    def test_assert_status_fails(self):
        response = Response(404, {}, "", {}, 100)
        with pytest.raises(AssertionError, match="Expected status 200"):
            assert_status(response, 200)

    def test_assert_json_contains_key(self):
        response = Response(200, {"name": "test", "id": 1}, "", {}, 100)
        assert_json_contains(response, "name")  # Should not raise

    def test_assert_json_contains_key_value(self):
        response = Response(200, {"name": "test"}, "", {}, 100)
        assert_json_contains(response, "name", "test")  # Should not raise

    def test_assert_json_contains_fails(self):
        response = Response(200, {"other": "value"}, "", {}, 100)
        with pytest.raises(AssertionError, match="not found"):
            assert_json_contains(response, "name")

    def test_assert_response_time_passes(self):
        response = Response(200, {}, "", {}, 100)
        assert_response_time(response, 200)  # Should not raise

    def test_assert_response_time_fails(self):
        response = Response(200, {}, "", {}, 500)
        with pytest.raises(AssertionError, match="took 500ms"):
            assert_response_time(response, 100)
