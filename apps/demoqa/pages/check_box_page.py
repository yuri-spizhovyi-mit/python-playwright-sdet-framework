"""
Check Box page object for DemoQA application.
"""

from playwright.sync_api import Page, expect
from apps.demoqa.pages.base_demoqa_page import BaseDemoQAPage


class CheckBoxPage(BaseDemoQAPage):
    """
    Page object representing the Check Box page.

    Responsibility:
    - Interact with the checkbox tree
    - Select items
    - Read selected result output
    """

    URL_PATH = "checkbox"

    # ---------- Page readiness ----------
    PAGE_HEADER = "h1:text('Check Box')"

    # ---------- Controls ----------
    EXPAND_ALL_BTN = "button[title='Expand all']"
    COLLAPSE_ALL_BTN = "button[title='Collapse all']"

    # ---------- Tree ----------
    TREE_ROOT = ".rct-tree"
    TREE_NODE = ".rct-node"
    TREE_LABEL = "label"
    NODE_LABEL = ".rct-title"
    CHECKBOX = ".rct-checkbox"

    # ---------- Output ----------
    RESULT_CONTAINER = "#result"
    RESULT_ITEMS = "#result span.text-success"

    def __init__(self, page: Page):
        super().__init__(page)
        self._assert_page_ready()

    # ---------- Readiness ----------

    def _assert_page_ready(self) -> None:
        expect(self.page.locator(self.PAGE_HEADER)).to_be_visible()

    # ---------- Actions ----------

    def expand_all(self) -> None:
        self.page.click(self.EXPAND_ALL_BTN)

    def collapse_all(self) -> None:
        self.page.click(self.COLLAPSE_ALL_BTN)

    def select(self, item_name: str) -> None:
        """
        Select a checkbox item by visible label text.
        """
        label = (
            self.page.locator(self.TREE_LABEL)
            .filter(has=self.page.locator(self.NODE_LABEL, has_text=item_name))
            .first
        )

        label.locator(self.CHECKBOX).click()

    # ---------- Queries ----------

    def selected_items(self) -> list[str]:
        """
        Return list of selected item names from the result panel.
        """
        return self.page.locator(self.RESULT_ITEMS).all_inner_texts()
