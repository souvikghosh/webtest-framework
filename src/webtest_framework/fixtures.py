"""Pytest fixtures for the testing framework."""

import os
from pathlib import Path
from typing import Generator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright

from .config import Config


@pytest.fixture(scope="session")
def config() -> Config:
    """Load test configuration."""
    config_path = Path("config.yaml")
    if config_path.exists():
        return Config.from_yaml(config_path)
    return Config.from_env()


@pytest.fixture(scope="session")
def browser_type_launch_args(config: Config) -> dict:
    """Browser launch arguments."""
    return {
        "headless": config.browser.headless,
        "slow_mo": config.browser.slow_mo,
    }


@pytest.fixture(scope="session")
def browser_context_args(config: Config) -> dict:
    """Browser context arguments."""
    return {
        "viewport": config.get_viewport(),
        "base_url": config.base_url,
    }


@pytest.fixture
def screenshot_dir(config: Config) -> Path:
    """Get screenshot directory, creating if needed."""
    path = Path(config.screenshot_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


@pytest.fixture
def take_screenshot(page: Page, screenshot_dir: Path, request):
    """Fixture to take screenshots on test failure."""
    yield

    if request.node.rep_call.failed:
        screenshot_path = screenshot_dir / f"{request.node.name}.png"
        page.screenshot(path=str(screenshot_path), full_page=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store test result on the item for screenshot fixture."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
