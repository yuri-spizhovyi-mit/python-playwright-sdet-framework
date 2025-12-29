import pytest
from api.postman_echo.client import EchoClient


@pytest.fixture(scope="session")
def echo_client() -> EchoClient:
    """
    Postman Echo API client.
    Session-scoped for speed and determinism.
    """
    return EchoClient()
