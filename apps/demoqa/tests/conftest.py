# apps/demoqa/tests/conftest.py

import pytest
from utils.data_generator import full_name, email, address


@pytest.fixture
def drag_offsets():
    """
    Standard drag distances for DemoQA drag tests.
    """
    return {
        "small": (50, 30),
        "medium": (100, 50),
        "large": (200, 100),
    }


@pytest.fixture
def selectable_indexes():
    """
    Common selectable item indexes.
    """
    return {
        "single": 1,
        "multi": [0, 2, 4],
    }


@pytest.fixture
def date_values():
    return {
        "simple": "12/25/2025",
        "date_time": "December 25, 2025 10:30 AM",
    }


@pytest.fixture
def slider_values():
    return [0, 25, 50, 75, 100]


@pytest.fixture
def date_picker_values():
    return {
        "date": "12/25/2025",
        "date_time": "December 25, 2025 10:30 AM",
    }


@pytest.fixture
def text_box_form_data():
    """
    Test data for DemoQA Text Box form.

    Generated dynamically to avoid hardcoded values
    while keeping test intent explicit.
    """
    return {
        "full_name": full_name(),
        "email": email(),
        "current_address": address(),
        "permanent_address": address(),
    }


@pytest.fixture
def resize_offsets():
    return {
        "restricted": (50, 50),
        "free": (100, 80),
    }


@pytest.fixture
def sortable_reorder_indexes():
    """
    Indexes used for list reorder validation.
    """
    return {
        "from": 0,
        "to": 3,
    }


@pytest.fixture
def checkbox_items():
    return {
        "single": "Desktop",
        "multiple": ["Documents", "Downloads"],
    }


@pytest.fixture
def radio_values():
    return {
        "yes": "Yes",
        "impressive": "Impressive",
    }
