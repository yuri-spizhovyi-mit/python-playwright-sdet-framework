"""
Droppable interaction page for DemoQA application.
"""

from playwright.sync_api import Page, expect
from apps.demoqa.pages.base_demoqa_page import BaseDemoQAPage


class DroppablePage(BaseDemoQAPage):
    """
    Page object representing the Droppable interaction.

    Responsibility:
    - Perform drag-and-drop actions across Droppable tabs
    - Expose drop result state via stable, behavior-based queries
    """

    URL_PATH = "droppable"

    # ---------- Page readiness ----------
    PAGE_HEADER = "h1:text('Droppable')"

    # ---------- Drop states ----------
    DROPPED_CLASS = "ui-state-highlight"
    DROPPED_TEXT = "Dropped!"

    # ---------- Tabs ----------
    SIMPLE_TAB = "#droppableExample-tab-simple"
    ACCEPT_TAB = "#droppableExample-tab-accept"
    REVERT_TAB = "#droppableExample-tab-revertable"

    # ---------- Tab panes ----------
    SIMPLE_PANE = "#droppableExample-tabpane-simple"
    ACCEPT_PANE = "#droppableExample-tabpane-accept"
    REVERT_PANE = "#droppableExample-tabpane-revertable"

    # ---------- Simple tab ----------
    SIMPLE_DRAGGABLE = "#droppableExample-tabpane-simple #draggable"
    SIMPLE_DROPPABLE = "#droppableExample-tabpane-simple #droppable"

    # ---------- Accept tab ----------
    ACCEPTABLE = "#droppableExample-tabpane-accept #acceptable"
    NOT_ACCEPTABLE = "#droppableExample-tabpane-accept #notAcceptable"
    ACCEPT_DROPPABLE = "#droppableExample-tabpane-accept #droppable"

    # ---------- Revert tab ----------
    REVERT_DRAGGABLE = "#droppableExample-tabpane-revertable #revertable"
    REVERT_DROPPABLE = "#droppableExample-tabpane-revertable #droppable"

    # ---------- Readiness ----------

    def _assert_page_ready(self) -> None:
        """
        Verify Droppable page base readiness (Simple tab).
        """
        expect(self.page.locator(self.PAGE_HEADER)).to_be_visible()
        expect(self.page.locator(self.SIMPLE_PANE)).to_be_visible()
        expect(self.page.locator(self.SIMPLE_DRAGGABLE)).to_be_visible()
        expect(self.page.locator(self.SIMPLE_DROPPABLE)).to_be_visible()

    # ---------- Navigation ----------

    def open_page(self) -> "DroppablePage":
        self.open(self.URL_PATH)
        self._assert_page_ready()
        return self

    def open_accept_tab(self) -> "DroppablePage":
        self.page.locator(self.ACCEPT_TAB).click()
        expect(self.page.locator(self.ACCEPT_PANE)).to_be_visible()
        return self

    def open_revert_tab(self) -> "DroppablePage":
        self.page.locator(self.REVERT_TAB).click()
        expect(self.page.locator(self.REVERT_PANE)).to_be_visible()
        return self

    # ---------- Actions ----------

    def drag_simple(self) -> None:
        self._drag(self.SIMPLE_DRAGGABLE, self.SIMPLE_DROPPABLE)

    def drag_acceptable(self) -> None:
        self._drag(self.ACCEPTABLE, self.ACCEPT_DROPPABLE)

    def drag_not_acceptable(self) -> None:
        self._drag(self.NOT_ACCEPTABLE, self.ACCEPT_DROPPABLE)

    def drag_revertable(self) -> None:
        self._drag(self.REVERT_DRAGGABLE, self.REVERT_DROPPABLE)

    # ---------- Queries ----------

    def simple_drop_success(self) -> bool:
        return self._drop_success(self.SIMPLE_DROPPABLE)

    def accept_drop_success(self) -> bool:
        return self._drop_success(self.ACCEPT_DROPPABLE)

    def wait_until_reverted(self, origin_x: float, tolerance: float = 5) -> float:
        """
        Wait until revertable draggable returns close to its original x-position.
        """
        locator = self.page.locator(self.REVERT_DRAGGABLE)

        self.page.wait_for_function(
            """
            ([selector, originX, tolerance]) => {
                const el = document.querySelector(selector);
                if (!el) return false;
                const rect = el.getBoundingClientRect();
                return Math.abs(rect.x - originX) <= tolerance;
            }
            """,
            arg=[self.REVERT_DRAGGABLE, origin_x, tolerance],
            timeout=3000,
        )

        box = locator.bounding_box()
        assert box, "Revert draggable bounding box not found after revert"
        return box["x"]

    # ---------- Internal helpers ----------

    def _drop_success(self, droppable_selector: str) -> bool:
        target = self.page.locator(droppable_selector)
        return (
            target.inner_text() == self.DROPPED_TEXT
            and self.DROPPED_CLASS in target.get_attribute("class")
        )

    def _drag(self, source_selector: str, target_selector: str) -> None:
        source = self.page.locator(source_selector)
        target = self.page.locator(target_selector)

        source.scroll_into_view_if_needed()
        target.scroll_into_view_if_needed()

        sb = source.bounding_box()
        tb = target.bounding_box()
        assert sb and tb, "Bounding box not available for drag operation"

        mouse = self.page.mouse
        mouse.move(sb["x"] + sb["width"] / 2, sb["y"] + sb["height"] / 2)
        mouse.down()
        mouse.move(tb["x"] + tb["width"] / 2, tb["y"] + tb["height"] / 2)
        mouse.up()
