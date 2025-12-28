"""
Resizable interaction page for DemoQA application.
"""

from playwright.sync_api import Page, expect
from apps.demoqa.pages.base_demoqa_page import BaseDemoQAPage


class ResizablePage(BaseDemoQAPage):
    """
    Page object representing the Resizable interaction.

    Responsibility:
    - Resize elements
    - Read element dimensions
    """

    URL_PATH = "resizable"

    # ---------- Page readiness ----------
    PAGE_HEADER = "h1:text('Resizable')"

    # ---------- Resizable boxes ----------
    RESIZABLE_BOX = "#resizableBoxWithRestriction"
    RESIZABLE_HANDLE = "#resizableBoxWithRestriction span.react-resizable-handle"

    RESIZABLE_FREE = "#resizable"
    RESIZABLE_FREE_HANDLE = "#resizable span.react-resizable-handle"

    def __init__(self, page: Page):
        super().__init__(page)
        self._assert_page_ready()

    # ---------- Readiness ----------

    def _assert_page_ready(self) -> None:
        expect(self.page.locator(self.PAGE_HEADER)).to_be_visible()
        expect(self.page.locator(self.RESIZABLE_BOX)).to_be_visible()

    # ---------- Navigation ----------

    def open_page(self) -> "ResizablePage":
        self.open(self.URL_PATH)
        return self

    # ---------- Actions ----------

    def _resize(self, handle_selector: str, dx: int, dy: int) -> None:
        handle = self.page.locator(handle_selector)
        box = handle.bounding_box()

        start_x = box["x"] + box["width"] / 2
        start_y = box["y"] + box["height"] / 2

        self.page.mouse.move(start_x, start_y)
        self.page.mouse.down()
        self.page.mouse.move(start_x + dx, start_y + dy)
        self.page.mouse.up()

    def resize_restricted_box(self, dx: int, dy: int) -> None:
        """
        Resize the restricted box by dragging its handle.
        """
        self._resize(self.RESIZABLE_HANDLE, dx, dy)

    def resize_free_box(self, dx: int, dy: int) -> None:
        """
        Resize the free box by dragging its handle.
        """
        self._resize(self.RESIZABLE_FREE_HANDLE, dx, dy)

    # ---------- Queries ----------

    def box_size(self) -> tuple[int, int]:
        """
        Return (width, height) of the restricted box.
        """
        box = self.page.locator(self.RESIZABLE_BOX).bounding_box()
        return int(box["width"]), int(box["height"])

    def free_box_size(self) -> tuple[int, int]:
        """
        Return (width, height) of the free resizable box.
        """
        box = self.page.locator(self.RESIZABLE_FREE).bounding_box()
        return int(box["width"]), int(box["height"])
