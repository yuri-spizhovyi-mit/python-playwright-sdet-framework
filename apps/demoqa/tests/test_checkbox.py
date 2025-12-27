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
def test_select_single_checkbox_item(page):
    """
    Verify that selecting a single checkbox item works.
    """
    elements_page = ElementsPage(page).open_page()
    elements_page.open_check_box()

    checkbox_page = CheckBoxPage(page)
    checkbox_page.expand_all()

    checkbox_page.select("Desktop")

    selected = checkbox_page.selected_items()

    assert "desktop" in [item.lower() for item in selected]


@pytest.mark.smoke
def test_select_multiple_checkbox_items(page):
    """
    Verify that multiple checkbox selections are reflected correctly.
    """
    elements_page = ElementsPage(page).open_page()
    elements_page.open_check_box()

    checkbox_page = CheckBoxPage(page)
    checkbox_page.expand_all()

    checkbox_page.select("Documents")
    checkbox_page.select("Downloads")

    selected = [item.lower() for item in checkbox_page.selected_items()]

    assert "documents" in selected
    assert "downloads" in selected
