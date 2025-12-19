from core.api_client import APIClient
from core.config import Config

class ReqResClient(APIClient):
    def __init__(self):
        super().__init__(Config.REQRES_URL)
