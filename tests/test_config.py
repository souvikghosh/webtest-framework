"""Tests for configuration module."""

import os
import pytest
from pathlib import Path

from webtest_framework.config import Config, BrowserConfig


class TestBrowserConfig:
    def test_defaults(self):
        config = BrowserConfig()
        assert config.headless is True
        assert config.slow_mo == 0
        assert config.viewport_width == 1280
        assert config.viewport_height == 720
        assert config.timeout == 30000

    def test_custom_values(self):
        config = BrowserConfig(
            headless=False,
            slow_mo=100,
            viewport_width=1920,
            viewport_height=1080,
        )
        assert config.headless is False
        assert config.slow_mo == 100
        assert config.viewport_width == 1920


class TestConfig:
    def test_defaults(self):
        config = Config()
        assert config.base_url == "http://localhost:8000"
        assert config.screenshot_on_failure is True
        assert isinstance(config.browser, BrowserConfig)

    def test_custom_base_url(self):
        config = Config(base_url="https://example.com")
        assert config.base_url == "https://example.com"

    def test_get_viewport(self):
        config = Config()
        viewport = config.get_viewport()
        assert viewport == {"width": 1280, "height": 720}

    def test_from_yaml_missing_file(self, tmp_path):
        config = Config.from_yaml(tmp_path / "missing.yaml")
        assert config.base_url == "http://localhost:8000"

    def test_from_yaml_valid_file(self, tmp_path):
        yaml_file = tmp_path / "config.yaml"
        yaml_file.write_text("base_url: https://test.com\n")

        config = Config.from_yaml(yaml_file)
        assert config.base_url == "https://test.com"

    def test_from_env(self, monkeypatch):
        monkeypatch.setenv("TEST_BASE_URL", "https://env.example.com")
        monkeypatch.setenv("TEST_HEADLESS", "false")
        monkeypatch.setenv("TEST_TIMEOUT", "60000")

        config = Config.from_env()
        assert config.base_url == "https://env.example.com"
        assert config.browser.headless is False
        assert config.browser.timeout == 60000
