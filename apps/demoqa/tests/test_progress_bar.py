"""
Tests for DemoQA Progress Bar widget.
"""

import pytest
from playwright.sync_api import expect

from apps.demoqa.pages.widgets_page import WidgetsPage
from apps.demoqa.pages.progress_bar_page import ProgressBarPage


@pytest.mark.smoke
def test_progress_bar_page_opens(page):
    """
    Verify Progress Bar page opens from Widgets menu.
    """
    WidgetsPage(page).open_page().open_progress_bar()
    ProgressBarPage(page)


@pytest.mark.smoke
def test_progress_bar_reaches_100_percent(page):
    """
    Verify progress bar can reach 100%.
    """
    WidgetsPage(page).open_page().open_progress_bar()
    progress_page = ProgressBarPage(page)

    progress_page.start()

    # Wait until progress reaches 100%
    expect(page.locator(progress_page.PROGRESS_BAR)).to_have_attribute(
        "aria-valuenow", "100", timeout=15_000
    )

    progress_page.reset()

    assert progress_page.progress_value() == 0
