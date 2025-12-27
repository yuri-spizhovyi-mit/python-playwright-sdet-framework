"""Tests for DemoQA Interaction widget."""

import pytest
from apps.demoqa.pages.interactions_page import InteractionsPage


@pytest.mark.smoke
def test_interactions_page_loads(page):
    """Interaction page load test"""
    interactions = InteractionsPage(page).open_page()
    assert interactions.is_loaded()
