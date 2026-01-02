"""
Tests for DemoQA Auto Complete widget.
"""

import pytest

from apps.demoqa.pages.widgets_page import WidgetsPage
from apps.demoqa.pages.auto_complete_page import AutoCompletePage


@pytest.mark.smoke
def test_auto_complete_page_opens_from_widgets_menu(page):
    """
    Verify Auto Complete page opens from Widgets menu.
    """
    WidgetsPage(page).open_page().open_auto_complete()

    # Readiness enforced in constructor
    AutoCompletePage(page)


@pytest.mark.smoke
def test_add_multiple_colors(page):
    """
    Verify multiple colors can be added.
    """
    WidgetsPage(page).open_page().open_auto_complete()
    auto_complete = AutoCompletePage(page)

    auto_complete.add_multi_color("Red")
    auto_complete.add_multi_color("Blue")
    selected = auto_complete.multi_selected_values()

    assert "Red" in selected
    assert "Blue" in selected


@pytest.mark.smoke
def test_set_single_color(page):
    """
    Verify single color can be selected.
    """
    WidgetsPage(page).open_page().open_auto_complete()
    auto_complete = AutoCompletePage(page)

    auto_complete.set_single_color("Green")

    assert auto_complete.single_selected_value() == "Green"
