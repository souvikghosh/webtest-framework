"""Custom assertions for test framework."""

from playwright.sync_api import Page, Locator, expect
import re


def expect_element(locator: Locator):
    """Get Playwright expect for a locator.

    Example:
        expect_element(page.locator("button")).to_be_visible()
    """
    return expect(locator)


def expect_url(page: Page, url_pattern: str | re.Pattern):
    """Assert page URL matches pattern.

    Args:
        page: Playwright page
        url_pattern: URL string or regex pattern
    """
    expect(page).to_have_url(url_pattern)


def expect_text(page: Page, text: str, selector: str | None = None):
    """Assert text is present on page.

    Args:
        page: Playwright page
        text: Text to find
        selector: Optional selector to search within
    """
    if selector:
        expect(page.locator(selector)).to_contain_text(text)
    else:
        expect(page.locator("body")).to_contain_text(text)


def expect_title(page: Page, title: str | re.Pattern):
    """Assert page title matches."""
    expect(page).to_have_title(title)


def expect_count(locator: Locator, count: int):
    """Assert number of matching elements."""
    expect(locator).to_have_count(count)


def expect_attribute(locator: Locator, attribute: str, value: str | re.Pattern):
    """Assert element has attribute with value."""
    expect(locator).to_have_attribute(attribute, value)


def expect_class(locator: Locator, class_name: str):
    """Assert element has CSS class."""
    expect(locator).to_have_class(re.compile(class_name))


def expect_enabled(locator: Locator):
    """Assert element is enabled."""
    expect(locator).to_be_enabled()


def expect_disabled(locator: Locator):
    """Assert element is disabled."""
    expect(locator).to_be_disabled()


def expect_checked(locator: Locator):
    """Assert checkbox is checked."""
    expect(locator).to_be_checked()


def expect_unchecked(locator: Locator):
    """Assert checkbox is unchecked."""
    expect(locator).not_to_be_checked()
