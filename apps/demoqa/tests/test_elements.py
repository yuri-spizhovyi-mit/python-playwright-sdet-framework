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
@pytest.mark.full
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
def test_text_box_form_submission(page, text_box_form_data):
    """
    Verify that Text Box form can be submitted and output is displayed.
    """
    ElementsPage(page).open_page().open_text_box()
    text_box_page = TextBoxPage(page)
    text_box_page.submit_form(**text_box_form_data)
    output = text_box_page.output_text()
    assert text_box_form_data["full_name"] in output
    assert text_box_form_data["email"] in output
    assert text_box_form_data["current_address"] in output
    assert text_box_form_data["permanent_address"] in output
