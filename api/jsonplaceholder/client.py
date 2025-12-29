from core.api_client import APIClient
from core.config import Config


class JsonPlaceholderClient(APIClient):
    def __init__(self):
        super().__init__(Config.JSONPLACEHOLDER_URL)

    def list_posts(self):
        return self.get("/posts")
