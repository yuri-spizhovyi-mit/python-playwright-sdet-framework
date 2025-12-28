"""
Droppable interaction page for DemoQA application.
"""

from playwright.sync_api import Page, expect
from apps.demoqa.pages.base_demoqa_page import BaseDemoQAPage


class DroppablePage(BaseDemoQAPage):
    """
    Page object representing the Droppable interaction.

    Responsibility:
    - Drag element to drop target
    - Read drop result state
    """

    URL_PATH = "droppable"

    # ---------- Page readiness ----------
    PAGE_HEADER = "h1:text('Droppable')"

    # ---------- Drag & Drop ----------
    DRAGGABLE = "#droppableExample-tabpane-simple #draggable"
    DROPPABLE = "#droppableExample-tabpane-simple #droppable"

    # ---------- Drop states ----------
    DROPPED_CLASS = "ui-state-highlight"
    DROPPED_TEXT = "Dropped!"

    def __init__(self, page: Page):
        super().__init__(page)
        self._assert_page_ready()
        
    # ---------- Tabs ----------
    SIMPLE_TAB = "#droppableExample-tab-simple"
    SIMPLE_TAB_PANE = "#droppableExample-tabpane-simple"


    # ---------- Readiness ----------

    def _assert_page_ready(self) -> None:
        expect(self.page.locator(self.PAGE_HEADER)).to_be_visible()
        expect(self.page.locator(self.SIMPLE_TAB_PANE)).to_be_visible()
        expect(self.page.locator(self.DRAGGABLE)).to_be_visible()
        expect(self.page.locator(self.DROPPABLE)).to_be_visible()

    # ---------- Navigation ----------

    def open_page(self) -> "DroppablePage":
        self.open(self.URL_PATH)
        return self

    # ---------- Actions ----------

    def drag_to_target(self) -> None:
        """
        Drag draggable element into the droppable target using mouse actions.
        """
        source = self.page.locator(self.DRAGGABLE).bounding_box()
        target = self.page.locator(self.DROPPABLE).bounding_box()

        start_x = source["x"] + source["width"] / 2
        start_y = source["y"] + source["height"] / 2

        end_x = target["x"] + target["width"] / 2
        end_y = target["y"] + target["height"] / 2

        mouse = self.page.mouse
        mouse.move(start_x, start_y)
        mouse.down()
        mouse.move(end_x, end_y)
        mouse.up()

    # ---------- Queries ----------

    def is_dropped(self) -> bool:
        """
        Return True if element was successfully dropped.
        """
        target = self.page.locator(self.DROPPABLE)
        return (
            target.inner_text() == self.DROPPED_TEXT
            and self.DROPPED_CLASS in target.get_attribute("class")
        )
