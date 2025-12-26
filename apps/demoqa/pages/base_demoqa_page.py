"""Base page for DemoQA application."""

from core.base_page import BasePage
from core.config import Config


class BaseDemoQAPage(BasePage):
    """Base page for DemoQA application."""

    def open(self, url: str):
        """
        Open a DemoQA page by relative path.
        """
        full_url = f"{Config.DEMOQA_URL.rstrip('/')}/{url.lstrip('/')}"
        self.page.goto(full_url)
        self.page.wait_for_load_state("domcontentloaded")
        return self
