"""
Sortable interaction page for DemoQA application.
"""

from typing import List
from playwright.sync_api import Page, expect

from apps.demoqa.pages.base_demoqa_page import BaseDemoQAPage


class SortablePage(BaseDemoQAPage):
    """
    Page object representing the Sortable interaction.

    Responsibility:
    - Read sortable item order
    - Perform reordering actions
    """

    URL_PATH = "sortable"

    # ---------- Page readiness ----------
    PAGE_HEADER = "h1:text('Sortable')"

    # ---------- Containers ----------
    LIST_CONTAINER = "#demo-tabpane-list"
    GRID_CONTAINER = "#demo-tabpane-grid"

    # ---------- Items ----------
    LIST_ITEMS = "#demo-tabpane-list .list-group-item"
    GRID_ITEMS = "#demo-tabpane-grid .list-group-item"

    # ---------- Tabs ----------
    LIST_TAB = "#demo-tab-list"
    GRID_TAB = "#demo-tab-grid"

    def __init__(self, page: Page):
        super().__init__(page)
        self._assert_page_ready()

    # ---------- Readiness ----------

    def _assert_page_ready(self) -> None:
        expect(self.page.locator(self.PAGE_HEADER)).to_be_visible()
        expect(self.page.locator(self.LIST_CONTAINER)).to_be_visible()

    # ---------- Navigation ----------

    def open_page(self) -> "SortablePage":
        """Open Sortable page directly."""
        self.open(self.URL_PATH)
        return self

    def open_grid(self) -> None:
        """Switch to Grid tab."""
        self.page.locator(self.GRID_TAB).click()
        expect(self.page.locator(self.GRID_CONTAINER)).to_be_visible()

    # ---------- Queries ----------

    def list_items_text(self) -> List[str]:
        """Return current list item order."""
        return self.page.locator(self.LIST_ITEMS).all_inner_texts()

    def grid_items_text(self) -> List[str]:
        """Return current grid item order."""
        return self.page.locator(self.GRID_ITEMS).all_inner_texts()

    # ---------- Actions ----------

    def drag_list_item(self, source_index: int, target_index: int) -> None:
        """
        Drag a list item from source_index to target_index.
        """
        items = self.page.locator(self.LIST_ITEMS)
        source = items.nth(source_index)
        target = items.nth(target_index)

        source.drag_to(target)
