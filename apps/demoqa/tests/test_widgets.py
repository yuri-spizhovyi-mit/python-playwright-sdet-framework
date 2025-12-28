"""Tests for DemoQA Widget."""

import pytest
from apps.demoqa.pages.widgets_page import WidgetsPage


@pytest.mark.smoke
def test_widgets_page_loads(page):
    """Widgets page load test"""
    interactions = WidgetsPage(page).open_page()
    assert interactions.is_loaded()
