"""Base page object for Page Object Model pattern."""

from typing import Self

from playwright.sync_api import Page, Locator, expect


class BasePage:
    """Base class for page objects.

    Implements the Page Object Model pattern for organized test code.
    """

    def __init__(self, page: Page, base_url: str = ""):
        """Initialize page object.

        Args:
            page: Playwright page instance
            base_url: Base URL for the application
        """
        self.page = page
        self.base_url = base_url

    @property
    def url(self) -> str:
        """Get current page URL."""
        return self.page.url

    @property
    def title(self) -> str:
        """Get page title."""
        return self.page.title()

    def navigate(self, path: str = "") -> Self:
        """Navigate to a path.

        Args:
            path: Path relative to base_url

        Returns:
            Self for chaining
        """
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}" if path else self.base_url
        self.page.goto(url)
        return self

    def wait_for_load(self) -> Self:
        """Wait for page to fully load."""
        self.page.wait_for_load_state("networkidle")
        return self

    def reload(self) -> Self:
        """Reload the page."""
        self.page.reload()
        return self

    def screenshot(self, path: str) -> Self:
        """Take a screenshot.

        Args:
            path: Path to save screenshot

        Returns:
            Self for chaining
        """
        self.page.screenshot(path=path, full_page=True)
        return self

    # Element interactions
    def click(self, selector: str) -> Self:
        """Click an element."""
        self.page.click(selector)
        return self

    def fill(self, selector: str, value: str) -> Self:
        """Fill a text field."""
        self.page.fill(selector, value)
        return self

    def type(self, selector: str, value: str, delay: int = 50) -> Self:
        """Type into a field character by character."""
        self.page.type(selector, value, delay=delay)
        return self

    def select(self, selector: str, value: str) -> Self:
        """Select an option from dropdown."""
        self.page.select_option(selector, value)
        return self

    def check(self, selector: str) -> Self:
        """Check a checkbox."""
        self.page.check(selector)
        return self

    def uncheck(self, selector: str) -> Self:
        """Uncheck a checkbox."""
        self.page.uncheck(selector)
        return self

    # Locator methods
    def locator(self, selector: str) -> Locator:
        """Get a locator for an element."""
        return self.page.locator(selector)

    def get_by_text(self, text: str, exact: bool = False) -> Locator:
        """Get element by text content."""
        return self.page.get_by_text(text, exact=exact)

    def get_by_role(self, role: str, **kwargs) -> Locator:
        """Get element by ARIA role."""
        return self.page.get_by_role(role, **kwargs)

    def get_by_label(self, label: str, exact: bool = False) -> Locator:
        """Get element by label."""
        return self.page.get_by_label(label, exact=exact)

    def get_by_placeholder(self, placeholder: str, exact: bool = False) -> Locator:
        """Get element by placeholder."""
        return self.page.get_by_placeholder(placeholder, exact=exact)

    def get_by_test_id(self, test_id: str) -> Locator:
        """Get element by data-testid attribute."""
        return self.page.get_by_test_id(test_id)

    # Waiting
    def wait_for(self, selector: str, state: str = "visible", timeout: int | None = None) -> Self:
        """Wait for element state.

        Args:
            selector: Element selector
            state: State to wait for (visible, hidden, attached, detached)
            timeout: Timeout in milliseconds
        """
        self.page.wait_for_selector(selector, state=state, timeout=timeout)
        return self

    def wait_for_url(self, url: str, timeout: int | None = None) -> Self:
        """Wait for URL to match."""
        self.page.wait_for_url(url, timeout=timeout)
        return self

    # Information
    def is_visible(self, selector: str) -> bool:
        """Check if element is visible."""
        return self.page.locator(selector).is_visible()

    def is_enabled(self, selector: str) -> bool:
        """Check if element is enabled."""
        return self.page.locator(selector).is_enabled()

    def text_content(self, selector: str) -> str | None:
        """Get text content of element."""
        return self.page.locator(selector).text_content()

    def get_attribute(self, selector: str, attribute: str) -> str | None:
        """Get attribute value of element."""
        return self.page.locator(selector).get_attribute(attribute)

    def count(self, selector: str) -> int:
        """Count matching elements."""
        return self.page.locator(selector).count()

    # Assertions using Playwright expect
    def expect_visible(self, selector: str) -> Self:
        """Assert element is visible."""
        expect(self.page.locator(selector)).to_be_visible()
        return self

    def expect_hidden(self, selector: str) -> Self:
        """Assert element is hidden."""
        expect(self.page.locator(selector)).to_be_hidden()
        return self

    def expect_text(self, selector: str, text: str) -> Self:
        """Assert element has text."""
        expect(self.page.locator(selector)).to_have_text(text)
        return self

    def expect_value(self, selector: str, value: str) -> Self:
        """Assert input has value."""
        expect(self.page.locator(selector)).to_have_value(value)
        return self
