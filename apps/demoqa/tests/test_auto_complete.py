"""
Tests for DemoQA Auto Complete widget.

Coverage:
- Navigation & readiness
- Suggestions behavior
- Selection (mouse + keyboard)
- Multi-value input
- Edge & stability cases
"""

import pytest

from apps.demoqa.pages.widgets_page import WidgetsPage
from apps.demoqa.pages.auto_complete_page import AutoCompletePage


# ---------------------------------------------------------------------------
# Navigation & readiness
# ---------------------------------------------------------------------------

@pytest.mark.smoke
def test_auto_complete_page_opens_from_widgets_menu(page):
    """
    Verify Auto Complete page opens from Widgets menu.
    """
    WidgetsPage(page).open_page().open_auto_complete()

    # Readiness enforced in constructor
    AutoCompletePage(page)


# ---------------------------------------------------------------------------
# Suggestions behavior
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "input_text, expected_present",
    [
        ("a", True),
        ("A", True),           # case-insensitive
        ("bl", True),
        ("zz", False),         # no matches
        ("@", False),          # special character
        ("1", False),          # numeric input
    ],
)
@pytest.mark.smoke
def test_suggestions_visibility_based_on_input(page, input_text, expected_present):
    """
    Verify suggestions appear or not depending on input.
    """
    WidgetsPage(page).open_page().open_auto_complete()
    auto_complete = AutoCompletePage(page)

    auto_complete.type_single(input_text)

    if expected_present:
        assert auto_complete.has_suggestions()
    else:
        assert not auto_complete.has_suggestions()


# ---------------------------------------------------------------------------
# Selection behavior (single value)
# ---------------------------------------------------------------------------

@pytest.mark.smoke
def test_select_value_with_mouse(page):
    """
    Verify value can be selected using mouse click.
    """
    WidgetsPage(page).open_page().open_auto_complete()
    auto_complete = AutoCompletePage(page)

    auto_complete.type_single("bl")
    auto_complete.select_suggestion("Black")

    assert auto_complete.single_value() == "Black"


@pytest.mark.smoke
def test_select_value_with_keyboard(page):
    """
    Verify value can be selected using keyboard (Enter).
    """
    WidgetsPage(page).open_page().open_auto_complete()
    auto_complete = AutoCompletePage(page)

    auto_complete.type_single("re")
    auto_complete.confirm_with_enter()

    assert auto_complete.single_value() == "Red"


@pytest.mark.smoke
def test_suggestions_close_after_selection(page):
    """
    Verify suggestions list closes after selection.
    """
    WidgetsPage(page).open_page().open_auto_complete()
    auto_complete = AutoCompletePage(page)

    auto_complete.type_single("gr")
    auto_complete.select_first_suggestion()

    assert not auto_complete.has_suggestions()


# ---------------------------------------------------------------------------
# Multi-value input behavior
# ---------------------------------------------------------------------------

@pytest.mark.smoke
def test_add_multiple_values(page):
    """
    Verify multiple values can be added.
    """
    WidgetsPage(page).open_page().open_auto_complete()
    auto_complete = AutoCompletePage(page)

    auto_complete.add_multiple(["Red", "Blue", "Green"])

    assert auto_complete.multi_values() == ["Red", "Blue", "Green"]


@pytest.mark.smoke
def test_prevent_duplicate_values(page):
    """
    Verify duplicate values are not added.
    """
    WidgetsPage(page).open_page().open_auto_complete()
    auto_complete = AutoCompletePage(page)

    auto_complete.add_multiple(["Red", "Red", "Blue"])

    assert auto_complete.multi_values() == ["Red", "Blue"]


@pytest.mark.smoke
def test_remove_value_from_multi_input(page):
    """
    Verify a selected value can be removed.
    """
    WidgetsPage(page).open_page().open_auto_complete()
    auto_complete = AutoCompletePage(page)

    auto_complete.add_multiple(["Red", "Blue"])
    auto_complete.remove_value("Red")

    assert auto_complete.multi_values() == ["Blue"]


# ---------------------------------------------------------------------------
# Edge & stability checks
# ---------------------------------------------------------------------------

@pytest.mark.smoke
def test_clear_input_resets_state(page):
    """
    Verify clearing input resets suggestions and value.
    """
    WidgetsPage(page).open_page().open_auto_complete()
    auto_complete = AutoCompletePage(page)

    auto_complete.type_single("bl")
    auto_complete.clear_single_input()

    assert auto_complete.single_value() == ""
    assert not auto_complete.has_suggestions()


@pytest.mark.smoke
def test_page_refresh_resets_auto_complete(page):
    """
    Verify page refresh resets Auto Complete state.
    """
    WidgetsPage(page).open_page().open_auto_complete()
    auto_complete = AutoCompletePage(page)

    auto_complete.add_multiple(["Red", "Blue"])

    page.reload()
    auto_complete = AutoCompletePage(page)

    assert auto_complete.multi_values() == []
