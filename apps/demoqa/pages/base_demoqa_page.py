"""Base page for DemoQA application."""

from typing import Self
from core.base_page import BasePage
from core.config import Config


class BaseDemoQAPage(BasePage):
    """Base page for DemoQA application."""

    URL_PATH: str | None = None

    def open(self, url: str):
        """
        Open a DemoQA page by relative path.
        """
        full_url = f"{Config.DEMOQA_URL.rstrip('/')}/{url.lstrip('/')}"
        self.page.goto(full_url)
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def open_page(self) -> Self:
        """Open page using its URL_PATH."""
        if not self.URL_PATH:
            raise ValueError(f"{self.__class__.__name__} must define URL_PATH")

        return self.open(self.URL_PATH)
