"""Tests for BasePage module."""

import pytest
from unittest.mock import MagicMock, PropertyMock

from webtest_framework.page import BasePage


@pytest.fixture
def mock_page():
    """Create mock Playwright page."""
    page = MagicMock()
    page.url = "http://localhost:8000/test"
    page.title.return_value = "Test Page"
    return page


@pytest.fixture
def base_page(mock_page):
    """Create BasePage with mock."""
    return BasePage(mock_page, "http://localhost:8000")


class TestBasePage:
    def test_url_property(self, base_page):
        assert base_page.url == "http://localhost:8000/test"

    def test_title_property(self, base_page, mock_page):
        assert base_page.title == "Test Page"
        mock_page.title.assert_called_once()

    def test_navigate(self, base_page, mock_page):
        base_page.navigate("/dashboard")
        mock_page.goto.assert_called_with("http://localhost:8000/dashboard")

    def test_navigate_empty_path(self, base_page, mock_page):
        base_page.navigate()
        mock_page.goto.assert_called_with("http://localhost:8000")

    def test_wait_for_load(self, base_page, mock_page):
        base_page.wait_for_load()
        mock_page.wait_for_load_state.assert_called_with("networkidle")

    def test_reload(self, base_page, mock_page):
        base_page.reload()
        mock_page.reload.assert_called_once()

    def test_screenshot(self, base_page, mock_page):
        base_page.screenshot("test.png")
        mock_page.screenshot.assert_called_with(path="test.png", full_page=True)

    def test_click(self, base_page, mock_page):
        base_page.click("#button")
        mock_page.click.assert_called_with("#button")

    def test_fill(self, base_page, mock_page):
        base_page.fill("#input", "value")
        mock_page.fill.assert_called_with("#input", "value")

    def test_type(self, base_page, mock_page):
        base_page.type("#input", "text", delay=100)
        mock_page.type.assert_called_with("#input", "text", delay=100)

    def test_select(self, base_page, mock_page):
        base_page.select("#dropdown", "option1")
        mock_page.select_option.assert_called_with("#dropdown", "option1")

    def test_check(self, base_page, mock_page):
        base_page.check("#checkbox")
        mock_page.check.assert_called_with("#checkbox")

    def test_uncheck(self, base_page, mock_page):
        base_page.uncheck("#checkbox")
        mock_page.uncheck.assert_called_with("#checkbox")

    def test_locator(self, base_page, mock_page):
        mock_locator = MagicMock()
        mock_page.locator.return_value = mock_locator

        result = base_page.locator("#element")

        mock_page.locator.assert_called_with("#element")
        assert result == mock_locator

    def test_get_by_text(self, base_page, mock_page):
        base_page.get_by_text("Click me")
        mock_page.get_by_text.assert_called_with("Click me", exact=False)

    def test_get_by_role(self, base_page, mock_page):
        base_page.get_by_role("button", name="Submit")
        mock_page.get_by_role.assert_called_with("button", name="Submit")

    def test_wait_for(self, base_page, mock_page):
        base_page.wait_for("#element", state="visible", timeout=5000)
        mock_page.wait_for_selector.assert_called_with(
            "#element", state="visible", timeout=5000
        )

    def test_is_visible(self, base_page, mock_page):
        mock_locator = MagicMock()
        mock_locator.is_visible.return_value = True
        mock_page.locator.return_value = mock_locator

        result = base_page.is_visible("#element")

        assert result is True

    def test_text_content(self, base_page, mock_page):
        mock_locator = MagicMock()
        mock_locator.text_content.return_value = "Hello World"
        mock_page.locator.return_value = mock_locator

        result = base_page.text_content("#element")

        assert result == "Hello World"

    def test_count(self, base_page, mock_page):
        mock_locator = MagicMock()
        mock_locator.count.return_value = 5
        mock_page.locator.return_value = mock_locator

        result = base_page.count(".items")

        assert result == 5

    def test_method_chaining(self, base_page, mock_page):
        """Test that methods return self for chaining."""
        result = (
            base_page
            .navigate("/path")
            .wait_for_load()
            .click("#button")
            .fill("#input", "value")
        )
        assert result is base_page
