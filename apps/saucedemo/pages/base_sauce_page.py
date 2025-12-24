"""
Base page object for SauceDemo UI automation.
Defines navigation and initialization shared by all SauceDemo page objects.
"""

from core.config import Config


class BaseSaucePage:
    """Base class for Sauce Demo page objects providing navigation convenience methods."""

    def __init__(self, page):
        """Initialize the BaseSaucePage with a Playwright page instance."""
        self.page = page

    def open(self, path: str = ""):
        """Open a specified path relative to the SAUCE_URL and wait for page load."""
        url = Config.SAUCE_URL.rstrip("/") + ("/" + path.lstrip("/") if path else "")
        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded")
