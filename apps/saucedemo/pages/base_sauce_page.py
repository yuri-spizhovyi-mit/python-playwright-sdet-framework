"""
Base page abstraction for SauceDemo application.
"""

from playwright.sync_api import Page

from core.base_page import BasePage
from core.config import Config


class BaseSaucePage(BasePage):
    """Common navigation behavior for SauceDemo pages."""

    def __init__(self, page: Page):
        super().__init__(page)

    def open(self, path: str = ""):
        """
        Open a SauceDemo page using a relative path.
        """
        base_url = Config.SAUCE_URL.rstrip("/")
        path = path.lstrip("/")

        url = f"{base_url}/{path}" if path else base_url
        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded")
