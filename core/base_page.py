"""
BasePage
--------
Common UI actions and safe wrappers around Playwright Page API.
All page objects must inherit from this class.
"""

from playwright.sync_api import Page, expect


class BasePage:
    """Base class for all UI page objects."""

    def __init__(self, page: Page):
        self.page = page

    # -------------------------
    # Navigation
    # -------------------------

    def open(self, url: str):
        """Navigate to a full URL."""
        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded")

    def refresh(self):
        """Refresh current page."""
        self.page.reload()
        self.page.wait_for_load_state("domcontentloaded")

    # -------------------------
    # Element actions
    # -------------------------

    def click(self, selector: str):
        """Click element after ensuring it is visible."""
        self.wait_for_visible(selector)
        self.page.click(selector)

    def fill(self, selector: str, value: str):
        """Fill input field safely."""
        self.wait_for_visible(selector)
        self.page.fill(selector, value)

    def type(self, selector: str, value: str):
        """Type text with keyboard simulation."""
        self.wait_for_visible(selector)
        self.page.type(selector, value)

    # -------------------------
    # Waiting helpers
    # -------------------------

    def wait_for_visible(self, selector: str, timeout: int = 5000):
        """Wait until element becomes visible."""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)

    def wait_for_hidden(self, selector: str, timeout: int = 5000):
        """Wait until element disappears."""
        self.page.wait_for_selector(selector, state="hidden", timeout=timeout)

    def wait_for_url(self, url_part: str, timeout: int = 5000):
        """Wait until URL contains given value."""
        self.page.wait_for_url(f"**{url_part}**", timeout=timeout)

    # -------------------------
    # Assertions (lightweight)
    # -------------------------

    def is_visible(self, selector: str) -> bool:
        """Check if element is visible."""
        return self.page.is_visible(selector)

    def has_text(self, selector: str, text: str):
        """Assert element has specific text."""
        expect(self.page.locator(selector)).to_have_text(text)

    def contains_text(self, selector: str, text: str):
        """Assert element contains text."""
        expect(self.page.locator(selector)).to_contain_text(text)
