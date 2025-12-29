import pytest
from api.jsonplaceholder.client import JsonPlaceholderClient


@pytest.fixture(scope="session")
def jsonplaceholder_client() -> JsonPlaceholderClient:
    """
    JSONPlaceholder API client fixture.
    Session-scoped for speed and determinism.
    """
    return JsonPlaceholderClient()
