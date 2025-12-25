"""
Pytest configuration and fixtures for SauceDemo application tests.
"""

import pytest
from core.config import Config


@pytest.fixture
def sauce_creds():
    """Fixture providing SauceDemo username and password from config."""
    return (Config.SAUCE_USERNAME, Config.SAUCE_PASSWORD)
