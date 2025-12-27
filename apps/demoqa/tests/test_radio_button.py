"""
Tests for DemoQA Radio Button page.
"""

import pytest

from apps.demoqa.pages.elements_page import ElementsPage
from apps.demoqa.pages.radio_button_page import RadioButtonPage


@pytest.mark.smoke
def test_radio_button_page_opens_from_elements_menu(page):
    """
    Verify that Radio Button page opens from Elements menu.
    """
    elements_page = ElementsPage(page).open_page()
    assert elements_page.is_loaded()

    elements_page.open_radio_button()

    # Page readiness enforced in constructor
    RadioButtonPage(page)


@pytest.mark.smoke
def test_select_yes_radio_button(page):
    """
    Verify selecting 'Yes' radio button.
    """
    ElementsPage(page).open_page().open_radio_button()
    radio_page = RadioButtonPage(page)

    radio_page.select_yes()

    assert radio_page.selected_value() == "Yes"


@pytest.mark.smoke
def test_select_impressive_radio_button(page):
    """
    Verify selecting 'Impressive' radio button.
    """
    ElementsPage(page).open_page().open_radio_button()
    radio_page = RadioButtonPage(page)

    radio_page.select_impressive()

    assert radio_page.selected_value() == "Impressive"


@pytest.mark.smoke
def test_no_radio_button_is_disabled(page):
    """
    Verify 'No' radio button cannot be selected.
    """
    ElementsPage(page).open_page().open_radio_button()
    radio_page = RadioButtonPage(page)

    radio_page.select_yes()
    assert radio_page.selected_value() == "Yes"

    radio_page.select_no()

    # Value must remain unchanged
    assert radio_page.selected_value() == "Yes"
