"""
Test suite for DemoQA Elements section.

Scope:
- Elements landing page loads correctly
- Text Box page can be opened via Elements navigation
- Text Box form submission works as expected

Notes:
- Navigation assertions belong to ElementsPage
- Content assertions belong to content pages (e.g. TextBoxPage)
"""

import pytest

from apps.demoqa.pages.elements_page import ElementsPage
from apps.demoqa.pages.text_box_page import TextBoxPage


@pytest.mark.smoke
def test_elements_page_loads(page):
    """
    Verify that the Elements landing page opens successfully.
    """
    elements_page = ElementsPage(page).open_page()

    assert elements_page.is_loaded()


@pytest.mark.smoke
def test_text_box_page_opens_from_elements_menu(page):
    """
    Verify that Text Box page can be opened from the Elements side menu.
    """
    elements_page = ElementsPage(page).open_page()
    assert elements_page.is_loaded()

    elements_page.open_text_box()

    # Page readiness is enforced inside TextBoxPage
    TextBoxPage(page)


@pytest.mark.smoke
def test_text_box_form_submission(page):
    """
    Verify that Text Box form can be submitted and output is displayed.
    """
    elements_page = ElementsPage(page).open_page()
    elements_page.open_text_box()

    text_box_page = TextBoxPage(page)

    text_box_page.submit_form(
        full_name="John Doe",
        email="john@doe.com",
        current_address="123 Main St",
        permanent_address="456 Oak Ave",
    )

    output = text_box_page.output_text()

    assert "John Doe" in output
    assert "john@doe.com" in output
    assert "123 Main St" in output
    assert "456 Oak Ave" in output
