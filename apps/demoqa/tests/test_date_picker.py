"""
Tests for DemoQA Date Picker widget.
"""

import pytest

from apps.demoqa.pages.widgets_page import WidgetsPage
from apps.demoqa.pages.date_picker_page import DatePickerPage


@pytest.mark.smoke
def test_date_picker_page_opens_from_widgets_menu(page):
    """
    Verify Date Picker page opens from Widgets menu.
    """
    WidgetsPage(page).open_page().open_date_picker()

    # Readiness enforced in constructor
    DatePickerPage(page)


@pytest.mark.smoke
def test_set_date(page, date_picker_values):
    """
    Verify that a date can be set in the Date Picker.
    """
    WidgetsPage(page).open_page().open_date_picker()
    date_picker = DatePickerPage(page)

    date_value = date_picker_values["date"]
    date_picker.set_date(date_value)

    assert date_picker.date_value() == date_value


@pytest.mark.smoke
def test_set_date_and_time(page, date_picker_values):
    """
    Verify that date and time can be set.
    """
    WidgetsPage(page).open_page().open_date_picker()
    date_picker = DatePickerPage(page)

    date_time_value = date_picker_values["date_time"]
    date_picker.set_date_time(date_time_value)

    assert date_picker.date_time_value() == date_time_value
