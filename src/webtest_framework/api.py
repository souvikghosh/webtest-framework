"""API testing utilities."""

from dataclasses import dataclass
from typing import Any

import requests


@dataclass
class Response:
    """API response wrapper."""

    status_code: int
    json_data: dict | list | None
    text: str
    headers: dict
    elapsed_ms: float

    @property
    def ok(self) -> bool:
        """Check if response was successful (2xx)."""
        return 200 <= self.status_code < 300

    def json(self) -> dict | list:
        """Get JSON data, raising if not available."""
        if self.json_data is None:
            raise ValueError("Response is not JSON")
        return self.json_data


class APIClient:
    """HTTP API client for testing APIs."""

    def __init__(self, base_url: str, timeout: int = 10):
        """Initialize API client.

        Args:
            base_url: Base URL for API
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.default_headers: dict[str, str] = {}

    def set_header(self, key: str, value: str) -> "APIClient":
        """Set a default header."""
        self.default_headers[key] = value
        return self

    def set_auth_token(self, token: str) -> "APIClient":
        """Set Bearer token authentication."""
        self.default_headers["Authorization"] = f"Bearer {token}"
        return self

    def _make_request(
        self,
        method: str,
        path: str,
        **kwargs,
    ) -> Response:
        """Make HTTP request."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        headers = {**self.default_headers, **kwargs.pop("headers", {})}

        response = self.session.request(
            method,
            url,
            headers=headers,
            timeout=self.timeout,
            **kwargs,
        )

        try:
            json_data = response.json()
        except ValueError:
            json_data = None

        return Response(
            status_code=response.status_code,
            json_data=json_data,
            text=response.text,
            headers=dict(response.headers),
            elapsed_ms=response.elapsed.total_seconds() * 1000,
        )

    def get(self, path: str, params: dict | None = None, **kwargs) -> Response:
        """Make GET request."""
        return self._make_request("GET", path, params=params, **kwargs)

    def post(self, path: str, json: Any = None, data: Any = None, **kwargs) -> Response:
        """Make POST request."""
        return self._make_request("POST", path, json=json, data=data, **kwargs)

    def put(self, path: str, json: Any = None, **kwargs) -> Response:
        """Make PUT request."""
        return self._make_request("PUT", path, json=json, **kwargs)

    def patch(self, path: str, json: Any = None, **kwargs) -> Response:
        """Make PATCH request."""
        return self._make_request("PATCH", path, json=json, **kwargs)

    def delete(self, path: str, **kwargs) -> Response:
        """Make DELETE request."""
        return self._make_request("DELETE", path, **kwargs)


def assert_status(response: Response, expected: int):
    """Assert response status code."""
    assert response.status_code == expected, (
        f"Expected status {expected}, got {response.status_code}"
    )


def assert_json_contains(response: Response, key: str, value: Any = None):
    """Assert JSON response contains key (and optionally value)."""
    data = response.json()
    assert isinstance(data, dict), "Response is not a JSON object"
    assert key in data, f"Key '{key}' not found in response"
    if value is not None:
        assert data[key] == value, f"Expected {key}={value}, got {data[key]}"


def assert_response_time(response: Response, max_ms: float):
    """Assert response time is within limit."""
    assert response.elapsed_ms <= max_ms, (
        f"Response took {response.elapsed_ms:.0f}ms, expected <= {max_ms}ms"
    )
