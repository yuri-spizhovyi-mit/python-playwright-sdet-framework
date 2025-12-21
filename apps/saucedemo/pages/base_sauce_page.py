# apps/saucedemo/pages/base_sauce_page.py
from core.config import Config


class BaseSaucePage:
    """Base class for Sauce Demo page objects providing navigation convenience methods."""

    def __init__(self, page):
        self.page = page

    def open(self, path: str = ""):
        url = Config.SAUCE_URL.rstrip("/") + ("/" + path.lstrip("/") if path else "")
        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded")
