import pytest

from apps.demoqa.pages.interactions_page import InteractionsPage
from apps.demoqa.pages.droppable_page import DroppablePage


@pytest.mark.smoke
def test_droppable_page_opens(page):
    """
    Verify Droppable page opens from Interactions menu.
    """
    InteractionsPage(page).open_page().open_droppable()
    DroppablePage(page)


@pytest.mark.full
def test_simple_drag_and_drop_success(page):
    """
    Verify draggable element can be dropped into target (Simple tab).
    """
    InteractionsPage(page).open_page().open_droppable()
    droppable = DroppablePage(page)

    droppable.drag_simple()

    assert droppable.simple_drop_success()


@pytest.mark.full
def test_accepts_only_valid_draggable(page):
    """
    Verify only acceptable draggable is accepted in Accept tab.
    """
    droppable = DroppablePage(page).open_page().open_accept_tab()

    droppable.drag_acceptable()
    assert droppable.accept_drop_success()


@pytest.mark.full
def test_revertable_draggable_returns_to_origin(page):
    """
    Verify revertable draggable returns to its original position.
    """

    droppable = DroppablePage(page).open_page().open_revert_tab()
    # Capture initial position
    before_x = droppable.page.locator(droppable.REVERT_DRAGGABLE).bounding_box()["x"]
    droppable.drag_revertable()
    # Wait for revert animation to complete
    after_x = droppable.wait_until_reverted(before_x)

    assert abs(after_x - before_x) < 5
