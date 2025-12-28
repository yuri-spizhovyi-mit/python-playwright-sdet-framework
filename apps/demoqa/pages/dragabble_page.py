"""
Draggable interaction page for DemoQA application.
"""

from playwright.sync_api import expect
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
        """
        Open the Dragabble page and verify it's ready.

        Returns:
            DragabblePage: Self for method chaining.
        """
        self.open(self.URL_PATH)
        self._assert_page_ready()
        return self

    def open_simple_tab(self):
        """
        Open the Simple tab and verify it's visible.

        Returns:
            DragabblePage: Self for method chaining.
        """
        self.page.locator(self.SIMPLE_TAB).click()
        expect(self.page.locator(self.SIMPLE_PANE)).to_be_visible()
        return self

    def open_axis_tab(self):
        """
        Open the Axis Restricted tab and verify it's visible.

        Returns:
            DragabblePage: Self for method chaining.
        """
        self.page.locator(self.AXIS_TAB).click()
        expect(self.page.locator(self.AXIS_PANE)).to_be_visible()
        return self

    def open_container_tab(self):
        """
        Open the Container Restricted tab and verify it's visible.

        Returns:
            DragabblePage: Self for method chaining.
        """
        self.page.locator(self.CONTAINER_TAB).click()
        expect(self.page.locator(self.CONTAINER_PANE)).to_be_visible()

        draggable = self.page.locator(self.CONTAINER_DRAGGABLE)
        draggable.scroll_into_view_if_needed()
        expect(draggable).to_be_visible()
        return self

    # ---------- Actions ----------

    def drag_simple(self, dx: int, dy: int):
        """
        Drag the simple draggable element by the specified offset.

        Args:
            dx: Horizontal offset in pixels.
            dy: Vertical offset in pixels.
        """
        self._drag(self.SIMPLE_DRAGGABLE, dx, dy)

    def drag_x_only(self, dx: int):
        """
        Drag the X-axis restricted draggable element horizontally.

        Args:
            dx: Horizontal offset in pixels.
        """
        self._drag(self.X_DRAGGABLE, dx, 0)

    def drag_y_only(self, dy: int):
        """
        Drag the Y-axis restricted draggable element vertically.

        Args:
            dy: Vertical offset in pixels.
        """
        self._drag(self.Y_DRAGGABLE, 0, dy)

    def drag_inside_container(self, dx: int, dy: int):
        """
        Drag the container-restricted draggable element by the specified offset.

        Args:
            dx: Horizontal offset in pixels.
            dy: Vertical offset in pixels.
        """
        self._drag(self.CONTAINER_DRAGGABLE, dx, dy)

    # ---------- Helpers ----------

    def _drag(self, selector: str, dx: int, dy: int):
        """
        Internal helper to drag an element by selector using mouse actions.

        Args:
            selector: CSS selector for the draggable element.
            dx: Horizontal offset in pixels.
            dy: Vertical offset in pixels.
        """
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
        """
        Verify that the page is loaded and ready by checking the page header.
        """
        expect(self.page.locator(self.PAGE_HEADER)).to_be_visible()

    def container_bounds(self) -> tuple[float, float, float, float]:
        """
        Returns (x, y, width, height) of the container restriction area.
        """
        box = self.page.locator(self.CONTAINER_PANE).bounding_box()
        assert box, "Container bounding box not found"
        return box["x"], box["y"], box["width"], box["height"]

    def draggable_bounds(self) -> tuple[float, float, float, float]:
        """
        Returns (x, y, width, height) of the container-restricted draggable.
        """
        box = self.page.locator(self.CONTAINER_DRAGGABLE).bounding_box()
        assert box, "Draggable bounding box not found"
        return box["x"], box["y"], box["width"], box["height"]
