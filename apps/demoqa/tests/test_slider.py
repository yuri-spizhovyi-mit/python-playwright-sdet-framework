"""
Tests for DemoQA Slider widget.
"""

import pytest

from apps.demoqa.pages.widgets_page import WidgetsPage
from apps.demoqa.pages.slider_page import SliderPage


@pytest.mark.smoke
def test_slider_page_opens_from_widgets_menu(page):
    """
    Verify that Slider page opens from Widgets menu.
    """
    widgets_page = WidgetsPage(page).open_page()
    assert widgets_page.is_loaded()

    widgets_page.open_slider()

    # Readiness enforced in constructor
    SliderPage(page)


@pytest.mark.smoke
@pytest.mark.parametrize("value", [0, 25, 50, 75, 100])
def test_set_slider_value(page, value):
    """
    Verify slider can be set to specific values.
    """
    WidgetsPage(page).open_page().open_slider()
    slider_page = SliderPage(page)

    slider_page.set_value(value)

    assert slider_page.current_value() == value
