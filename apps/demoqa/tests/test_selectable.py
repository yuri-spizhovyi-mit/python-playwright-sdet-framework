import pytest

from apps.demoqa.pages.interactions_page import InteractionsPage
from apps.demoqa.pages.selectable_page import SelectablePage


@pytest.mark.smoke
def test_selectable_page_opens(page):
    """
    Verify Selectable page opens from Interactions menu.
    """
    InteractionsPage(page).open_page().open_selectable()
    SelectablePage(page)


@pytest.mark.full
def test_single_item_selection(page, selectable_indexes):
    """
    Verify single list item selection.
    """
    InteractionsPage(page).open_page().open_selectable()
    selectable = SelectablePage(page)

    selectable.select_list_item(selectable_indexes["single"])

    selected = selectable.selected_list_items()
    assert selected == ["Dapibus ac facilisis in"]


@pytest.mark.full
def test_multi_select_grid_items(page):
    InteractionsPage(page).open_page().open_selectable()
    selectable = SelectablePage(page)

    selectable.select_grid_items([0, 2, 4])

    selected = selectable.selected_grid_items()
    assert len(selected) == 3
