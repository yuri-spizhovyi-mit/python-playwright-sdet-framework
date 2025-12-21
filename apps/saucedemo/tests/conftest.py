# App-specific fixtures
import pytest
from core.config import Config


@pytest.fixture
def sauce_creds():
    return (Config.SAUCE_USERNAME, Config.SAUCE_PASSWORD)
