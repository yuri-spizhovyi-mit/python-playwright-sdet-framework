"""
Tabs page object for DemoQA application.
"""

from playwright.sync_api import Page, expect
from apps.demoqa.pages.base_demoqa_page import BaseDemoQAPage
import re


class TabsPage(BaseDemoQAPage):
    """
    Page object representing the Tabs widget.
    """

    URL_PATH = "tabs"

    # ---------- Page readiness ----------
    PAGE_HEADER = "h1:text('Tabs')"

    # ---------- Tabs (stable IDs) ----------
    TAB_WHAT = "#demo-tab-what"
    TAB_ORIGIN = "#demo-tab-origin"
    TAB_USE = "#demo-tab-use"
    TAB_MORE = "#demo-tab-more"

    # ---------- Active state ----------
    ACTIVE_TAB = "a.nav-link[aria-selected='true']"
    ACTIVE_PANEL = "div.tab-pane[aria-hidden='false']"

    def __init__(self, page: Page):
        super().__init__(page)
        self._assert_page_ready()

    # ---------- Readiness ----------

    def _assert_page_ready(self) -> None:
        expect(self.page.locator(self.PAGE_HEADER)).to_be_visible()
        expect(self.page.locator(self.TAB_WHAT)).to_be_visible()

    # ---------- Actions ----------

    def open_what(self) -> None:
        self._open_tab(self.TAB_WHAT)

    def open_origin(self) -> None:
        self._open_tab(self.TAB_ORIGIN)

    def open_use(self) -> None:
        self._open_tab(self.TAB_USE)

    def _open_tab(self, selector: str) -> None:
        """
        Open tab by stable ID and wait for panel activation.
        """
        self.page.locator(selector).click()

        # Wait for real state change (panel becomes active)
        expect(self.page.locator(selector)).to_have_attribute("aria-selected", "true")
        # Wait for panel to be visible
        expect(self.page.locator(self.ACTIVE_PANEL)).to_be_visible()

    # ---------- Queries ----------

    def active_tab_name(self) -> str:
        """
        Return name of currently active tab.
        """
        return self.page.locator(self.ACTIVE_TAB).inner_text()

    def active_tab_content(self) -> str:
        """
        Return text content of active tab panel.
        """
        return self.page.locator(self.ACTIVE_PANEL).inner_text()

    def open_tab(self, name: str) -> None:
        """
        Open tab by logical name.
        """
        mapping = {
            "What": self.TAB_WHAT,
            "Origin": self.TAB_ORIGIN,
            "Use": self.TAB_USE,
        }

        if name not in mapping:
            raise ValueError(f"Unknown tab name: {name}")

        self._open_tab(mapping[name])
