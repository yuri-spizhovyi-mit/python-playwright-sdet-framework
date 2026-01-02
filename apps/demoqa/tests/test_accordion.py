"""
Tests for DemoQA Accordion widget.
"""

import pytest

from apps.demoqa.pages.widgets_page import WidgetsPage
from apps.demoqa.pages.accordion_page import AccordionPage


@pytest.mark.smoke
def test_accordion_page_opens_from_widgets_menu(page):
    """
    Verify Accordion page opens from Widgets menu.
    """
    WidgetsPage(page).open_page().open_accordian()

    # Readiness enforced in constructor
    AccordionPage(page)


@pytest.mark.smoke
def test_open_first_accordion_section(page):
    """
    Verify first accordion section can be opened.
    """
    WidgetsPage(page).open_page().open_accordian()
    accordion = AccordionPage(page)

    accordion.open_section(1)

    assert accordion.is_section_open(1)


@pytest.mark.smoke
def test_open_second_accordion_section(page):
    """
    Verify second accordion section can be opened.
    """
    WidgetsPage(page).open_page().open_accordian()
    accordion = AccordionPage(page)

    accordion.open_section(2)

    assert accordion.is_section_open(2)
