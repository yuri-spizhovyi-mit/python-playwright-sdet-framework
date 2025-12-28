import pytest

from apps.demoqa.pages.interactions_page import InteractionsPage
from apps.demoqa.pages.resizable_page import ResizablePage


@pytest.mark.smoke
def test_resizable_page_opens(page):
    """
    Verify Resizable page opens from Interactions menu.
    """
    InteractionsPage(page).open_page().open_resizable()
    ResizablePage(page)


@pytest.mark.full
def test_restricted_box_resizes(page, resize_offsets):
    """
    Verify restricted resizable box can be resized within limits.
    """
    InteractionsPage(page).open_page().open_resizable()
    resizable = ResizablePage(page)

    before = resizable.box_size()

    dx, dy = resize_offsets["restricted"]
    resizable.resize_restricted_box(dx, dy)

    after = resizable.box_size()

    assert after[0] > before[0]
    assert after[1] > before[1]


@pytest.mark.full
def test_free_box_resizes(page, resize_offsets):
    """
    Verify free resizable box can be resized.
    """
    InteractionsPage(page).open_page().open_resizable()
    resizable = ResizablePage(page)

    before = resizable.free_box_size()

    dx, dy = resize_offsets["free"]
    resizable.resize_free_box(dx, dy)

    after = resizable.free_box_size()

    assert after[0] > before[0]
    assert after[1] > before[1]
