"""Test suite for verifying the elements functionality of DemoQA using Playwright."""

import pytest
from apps.demoqa.pages.elements_page import ElementsPage


@pytest.mark.smoke
def test_elements_page_loads(page):
    """Verify Elements page opens successfully."""
    elements = ElementsPage(page).open(ElementsPage.URL_PATH)

    assert elements.is_loaded()
    assert elements.get_title() == "Elements"


@pytest.mark.smoke
def test_text_box_menu_opens(page):
    """Verify Text Box menu opens successfully."""
    elements = ElementsPage(page).open(ElementsPage.URL_PATH)
    elements.open_elements_item(ElementsPage.TEXT_BOX_MENU)

    elements.fill_text_box(
        name="John Doe",
        email="john.doe@example.com",
        address="123 Main St, New York, USA",
    )
    assert elements.is_loaded()
