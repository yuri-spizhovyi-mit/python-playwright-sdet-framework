from playwright.sync_api import expect
from typing import Tuple
from apps.demoqa.pages.base_demoqa_page import BaseDemoQAPage


class DragabblePage(BaseDemoQAPage):
    """Page object for DemoQA Dragabble page."""

    URL_PATH = "dragabble"

    # ---------- Page readiness ----------
    PAGE_HEADER = "h1:text('Dragabble')"

    # ---------- Tabs ----------
    SIMPLE_TAB = "#draggableExample-tab-simple"
    AXIS_TAB = "#draggableExample-tab-axisRestriction"
    CONTAINER_TAB = "#draggableExample-tab-containerRestriction"

    SIMPLE_PANE = "#draggableExample-tabpane-simple"
    AXIS_PANE = "#draggableExample-tabpane-axisRestriction"
    CONTAINER_PANE = "#draggableExample-tabpane-containerRestriction"

    # ---------- Draggables ----------
    SIMPLE_DRAGGABLE = "#draggableExample-tabpane-simple #dragBox"

    X_DRAGGABLE = "#draggableExample-tabpane-axisRestriction #restrictedX"
    Y_DRAGGABLE = "#draggableExample-tabpane-axisRestriction #restrictedY"

    CONTAINER_DRAGGABLE = (
        "#draggableExample-tabpane-containerRestriction "
        "#containmentWrapper div.draggable"
    )

    # ---------- Public API ----------

    def open_page(self):
        self.open(self.URL_PATH)
        self._assert_page_ready()
        return self

    def open_simple_tab(self):
        self.page.locator(self.SIMPLE_TAB).click()
        expect(self.page.locator(self.SIMPLE_PANE)).to_be_visible()
        return self

    def open_axis_tab(self):
        self.page.locator(self.AXIS_TAB).click()
        expect(self.page.locator(self.AXIS_PANE)).to_be_visible()
        return self

    def open_container_tab(self):
        self.page.locator(self.CONTAINER_TAB).click()
        expect(self.page.locator(self.CONTAINER_PANE)).to_be_visible()

        draggable = self.page.locator(self.CONTAINER_DRAGGABLE)
        draggable.scroll_into_view_if_needed()
        expect(draggable).to_be_visible()
        return self

    # ---------- Actions ----------

    def drag_simple(self, dx: int, dy: int):
        self._drag(self.SIMPLE_DRAGGABLE, dx, dy)

    def drag_x_only(self, dx: int):
        self._drag(self.X_DRAGGABLE, dx, 0)

    def drag_y_only(self, dy: int):
        self._drag(self.Y_DRAGGABLE, 0, dy)

    def drag_inside_container(self, dx: int, dy: int):
        self._drag(self.CONTAINER_DRAGGABLE, dx, dy)

    # ---------- Helpers ----------

    def _drag(self, selector: str, dx: int, dy: int):
        el = self.page.locator(selector)
        box = el.bounding_box()
        assert box, "Draggable bounding box not found"

        self.page.mouse.move(
            box["x"] + box["width"] / 2,
            box["y"] + box["height"] / 2,
        )
        self.page.mouse.down()
        self.page.mouse.move(
            box["x"] + box["width"] / 2 + dx,
            box["y"] + box["height"] / 2 + dy,
            steps=10,
        )
        self.page.mouse.up()

    def _assert_page_ready(self):
        expect(self.page.locator(self.PAGE_HEADER)).to_be_visible()
