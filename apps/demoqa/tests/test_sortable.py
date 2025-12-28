import pytest

from apps.demoqa.pages.interactions_page import InteractionsPage
from apps.demoqa.pages.sortable_page import SortablePage


@pytest.mark.smoke
def test_sortable_page_opens(page):
    """
    Verify Sortable page opens from Interactions menu.
    """
    InteractionsPage(page).open_page().open_sortable()
    SortablePage(page)


@pytest.mark.full
def test_sortable_list_reorder(page, sortable_reorder_indexes):
    """
    Verify list items can be reordered.
    """
    InteractionsPage(page).open_page().open_sortable()
    sortable = SortablePage(page)

    before = sortable.list_items_text()

    # Drag first item to position 3
    from_index = sortable_reorder_indexes["from"]
    to_index = sortable_reorder_indexes["to"]
    sortable.drag_list_item(from_index, to_index)

    after = sortable.list_items_text()

    assert before != after
    assert after[3] == before[0]


@pytest.mark.full
def test_sortable_grid_tab_loads(page):
    """
    Verify Grid tab opens and displays items.
    """
    InteractionsPage(page).open_page().open_sortable()
    sortable = SortablePage(page)

    sortable.open_grid()

    items = sortable.grid_items_text()
    assert len(items) > 0
