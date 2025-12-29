from core.api_client import APIClient
from core.config import Config


class EchoClient(APIClient):
    """
    Client for Postman Echo API.
    Used for deterministic API testing.
    """

    def __init__(self):
        super().__init__(Config.POSTMAN_ECHO_URL)

    def post_echo(self, payload: dict):
        return self.post("/post", json=payload)

    def get_headers(self):
        return self.get("/headers")
