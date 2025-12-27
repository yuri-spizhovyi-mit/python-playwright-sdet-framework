"""
Tests for DemoQA Tabs widget.
"""

import pytest

from apps.demoqa.pages.widgets_page import WidgetsPage
from apps.demoqa.pages.tabs_page import TabsPage


@pytest.mark.smoke
def test_tabs_page_opens_from_widgets_menu(page):
    """
    Verify Tabs page opens from Widgets menu.
    """
    WidgetsPage(page).open_page().open_tabs()

    # Readiness enforced in constructor
    TabsPage(page)


@pytest.mark.smoke
@pytest.mark.parametrize(
    "tab_name",
    ["What", "Origin", "Use"],
)
def test_switch_tabs(page, tab_name):
    """
    Verify switching between tabs updates active tab and content.
    """
    WidgetsPage(page).open_page().open_tabs()
    tabs_page = TabsPage(page)

    tabs_page.open_tab(tab_name)

    assert tabs_page.active_tab_name() == tab_name
    assert tabs_page.active_tab_content()
