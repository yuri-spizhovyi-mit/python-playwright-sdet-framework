"""
Selectable interaction page for DemoQA application.
"""

from typing import List
from playwright.sync_api import Page, expect

from apps.demoqa.pages.base_demoqa_page import BaseDemoQAPage


class SelectablePage(BaseDemoQAPage):
    """
    Page object representing the Selectable interaction.

    Responsibility:
    - Select one or multiple items
    - Read selected state
    """

    URL_PATH = "selectable"

    # ---------- Page readiness ----------
    PAGE_HEADER = "h1:text('Selectable')"

    # ---------- Tabs ----------
    LIST_TAB = "#demo-tab-list"
    GRID_TAB = "#demo-tab-grid"

    # ---------- Containers ----------
    LIST_CONTAINER = "#demo-tabpane-list"
    GRID_CONTAINER = "#demo-tabpane-grid"

    # ---------- Items ----------
    LIST_ITEMS = "#demo-tabpane-list .list-group-item"
    GRID_ITEMS = "#demo-tabpane-grid .list-group-item"

    # ---------- Selected state ----------
    SELECTED_CLASS = "active"

    def __init__(self, page: Page):
        super().__init__(page)
        self._assert_page_ready()

    # ---------- Readiness ----------

    def _assert_page_ready(self) -> None:
        expect(self.page.locator(self.PAGE_HEADER)).to_be_visible()
        expect(self.page.locator(self.LIST_CONTAINER)).to_be_visible()

    # ---------- Navigation ----------

    def open_page(self) -> "SelectablePage":
        self.open(self.URL_PATH)
        return self

    def open_grid(self) -> None:
        self.page.locator(self.GRID_TAB).click()
        expect(self.page.locator(self.GRID_CONTAINER)).to_be_visible()

    # ---------- Private helpers ----------

    def _list_items(self):
        return self.page.locator(self.LIST_ITEMS)

    def _grid_items(self):
        return self.page.locator(self.GRID_ITEMS)

    # ---------- Actions ----------

    def select_list_item(self, index: int) -> None:
        """Select a single list item."""
        self._list_items().nth(index).click()

    def multi_select_list_items(self, indices: List[int]) -> None:
        """Select multiple list items (List tab is effectively single-select in DemoQA)."""
        for index in indices:
            self._list_items().nth(index).click(modifiers=["Control"])

    def select_grid_items(self, indices: List[int]) -> None:
        """Select multiple grid items using modifier clicks."""
        self.open_grid()
        for index in indices:
            self._grid_items().nth(index).click(modifiers=["Control"])

    # ---------- Queries ----------

    def selected_list_items(self) -> List[str]:
        """
        Return list of text from selected list items.
        """
        return self.page.locator(
            f"{self.LIST_ITEMS}.{self.SELECTED_CLASS}"
        ).all_inner_texts()

    def selected_grid_items(self) -> List[str]:
        """
        Return list of text from selected grid items.
        """
        return self.page.locator(
            f"{self.GRID_ITEMS}.{self.SELECTED_CLASS}"
        ).all_inner_texts()

    def list_items_text(self) -> List[str]:
        """
        Return list of text from all list items.
        """
        return self._list_items().all_inner_texts()
