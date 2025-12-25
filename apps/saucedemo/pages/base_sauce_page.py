"""
Base page abstraction for SauceDemo application.
"""

from core.base_page import BasePage
from core.config import Config


class BaseSaucePage(BasePage):
    """Common navigation behavior for SauceDemo pages."""

    def open(self, url: str = ""):
        """
        Open a SauceDemo page using a relative path.
        """
        base_url = Config.SAUCE_URL.rstrip("/")
        url = url.lstrip("/")

        url = f"{base_url}/{url}" if url else base_url
        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded")
