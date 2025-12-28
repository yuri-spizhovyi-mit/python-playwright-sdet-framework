"""
Tests for DemoQA Check Box page.
"""

import pytest

from apps.demoqa.pages.elements_page import ElementsPage
from apps.demoqa.pages.check_box_page import CheckBoxPage


@pytest.mark.smoke
def test_checkbox_page_opens_from_elements_menu(page):
    """
    Verify that Check Box page can be opened from Elements menu.
    """
    elements_page = ElementsPage(page).open_page()
    assert elements_page.is_loaded()

    elements_page.open_check_box()

    # Page readiness enforced in constructor
    CheckBoxPage(page)


@pytest.mark.smoke
def test_select_single_checkbox_item(page, checkbox_items):
    """
    Verify that selecting a single checkbox item works.
    """
    ElementsPage(page).open_page().open_check_box()
    checkbox_page = CheckBoxPage(page)
    checkbox_page.expand_all()

    checkbox_page.select(checkbox_items["single"])

    selected = [item.lower() for item in checkbox_page.selected_items()]
    assert checkbox_items["single"].lower() in selected


@pytest.mark.smoke
def test_select_multiple_checkbox_items(page, checkbox_items):
    """
    Verify that multiple checkbox selections are reflected correctly.
    """
    ElementsPage(page).open_page().open_check_box()
    checkbox_page = CheckBoxPage(page)
    checkbox_page.expand_all()

    for item in checkbox_items["multiple"]:
        checkbox_page.select(item)

    selected = [item.lower() for item in checkbox_page.selected_items()]

    for item in checkbox_items["multiple"]:
        assert item.lower() in selected
