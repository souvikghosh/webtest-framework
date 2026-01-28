"""Configuration management for test framework."""

import os
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel


class BrowserConfig(BaseModel):
    """Browser configuration."""

    headless: bool = True
    slow_mo: int = 0
    viewport_width: int = 1280
    viewport_height: int = 720
    timeout: int = 30000


class Config(BaseModel):
    """Test framework configuration."""

    base_url: str = "http://localhost:8000"
    browser: BrowserConfig = BrowserConfig()
    screenshot_on_failure: bool = True
    screenshot_dir: str = "screenshots"
    api_timeout: int = 10

    @classmethod
    def from_yaml(cls, path: str | Path) -> "Config":
        """Load configuration from YAML file."""
        path = Path(path)
        if not path.exists():
            return cls()

        with open(path) as f:
            data = yaml.safe_load(f)

        return cls(**data) if data else cls()

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        config_data: dict[str, Any] = {}

        if base_url := os.getenv("TEST_BASE_URL"):
            config_data["base_url"] = base_url

        if headless := os.getenv("TEST_HEADLESS"):
            config_data.setdefault("browser", {})["headless"] = headless.lower() == "true"

        if timeout := os.getenv("TEST_TIMEOUT"):
            config_data.setdefault("browser", {})["timeout"] = int(timeout)

        return cls(**config_data)

    def get_viewport(self) -> dict[str, int]:
        """Get viewport size as dict."""
        return {
            "width": self.browser.viewport_width,
            "height": self.browser.viewport_height,
        }
