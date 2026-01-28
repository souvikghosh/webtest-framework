"""Example page object for demonstration."""

from webtest_framework import BasePage


class SearchPage(BasePage):
    """Example page object for a search page."""

    # Selectors
    SEARCH_INPUT = "input[name='q']"
    SEARCH_BUTTON = "button[type='submit']"
    RESULTS_LIST = ".search-results"
    RESULT_ITEM = ".search-results .result-item"
    NO_RESULTS = ".no-results"

    def search(self, query: str):
        """Perform a search.

        Args:
            query: Search query string

        Returns:
            Self for chaining
        """
        return (
            self.fill(self.SEARCH_INPUT, query)
            .click(self.SEARCH_BUTTON)
            .wait_for_load()
        )

    def get_result_count(self) -> int:
        """Get number of search results."""
        return self.count(self.RESULT_ITEM)

    def expect_results(self, min_count: int = 1):
        """Assert that search returned results.

        Args:
            min_count: Minimum expected results
        """
        self.expect_visible(self.RESULTS_LIST)
        assert self.get_result_count() >= min_count
        return self

    def expect_no_results(self):
        """Assert that search returned no results."""
        self.expect_visible(self.NO_RESULTS)
        return self

    def click_result(self, index: int = 0):
        """Click a search result by index."""
        items = self.locator(self.RESULT_ITEM)
        items.nth(index).click()
        return self
