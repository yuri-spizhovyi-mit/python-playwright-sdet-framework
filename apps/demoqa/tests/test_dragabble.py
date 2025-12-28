import pytest
from apps.demoqa.pages.dragabble_page import DragabblePage


@pytest.mark.smoke
def test_simple_drag(page):
    dragabble = DragabblePage(page).open_page().open_simple_tab()
    dragabble.drag_simple(100, 50)


def test_axis_restricted_drag(page):
    dragabble = DragabblePage(page).open_page().open_axis_tab()
    dragabble.drag_x_only(120)
    dragabble.drag_y_only(80)


def test_container_restricted_drag(page):
    dragabble = DragabblePage(page).open_page().open_container_tab()

    # Act
    dragabble.drag_inside_container(200, 200)

    # Assert: draggable stays within container bounds
    cx, cy, cw, ch = dragabble.container_bounds()
    dx, dy, dw, dh = dragabble.draggable_bounds()

    assert dx >= cx
    assert dy >= cy
    assert dx + dw <= cx + cw
    assert dy + dh <= cy + ch


def test_cursor_style_drag(page):
    """
    Verify draggable elements move correctly under different cursor styles.
    This is a resilience test, not a visual test.
    """
    dragabble = DragabblePage(page).open_page().open_cursor_tab()

    dragabble.drag_cursor_center(80, 40)
    dragabble.drag_cursor_top_left(60, 30)
    dragabble.drag_cursor_bottom(50, 25)
