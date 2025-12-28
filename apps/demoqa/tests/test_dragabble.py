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
