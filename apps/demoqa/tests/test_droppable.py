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
def test_drag_and_drop_success(page):
    """
    Verify draggable element can be dropped into target.
    """
    InteractionsPage(page).open_page().open_droppable()
    droppable = DroppablePage(page)

    droppable.drag_to_target()

    assert droppable.is_dropped()
