"""WebTest Framework - Web application testing with Playwright."""

__version__ = "1.0.0"

from .page import BasePage
from .config import Config
from .assertions import expect_element, expect_url, expect_text

__all__ = ["BasePage", "Config", "expect_element", "expect_url", "expect_text"]
