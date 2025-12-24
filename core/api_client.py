# core/api_client.py

from __future__ import annotations

import time
from typing import Any, Dict, Optional

import requests
from requests import Response, Session

from core.config import Config
from core.logger import get_logger


class APIClient:
    """
    Thin HTTP client abstraction for API testing.

    Responsibilities:
    - Manage HTTP session lifecycle
    - Centralize base URL, headers, timeout
    - Log requests and responses
    - Return raw Response objects (no assertions)

    NOT responsible for:
    - Test assertions
    - Schema validation
    - Business logic checks
    """

    def __init__(
        self,
        base_url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout or Config.API_TIMEOUT

        self.session: Session = requests.Session()
        self.session.headers.update(headers or {})

        self.logger = get_logger(self.__class__.__name__)

        self.logger.info(
            f"APIClient initialized | base_url={self.base_url}, timeout={self.timeout}s"
        )

    # ------------------------------------------------------------------
    # Public HTTP methods
    # ------------------------------------------------------------------

    def get(self, path: str, **kwargs) -> Response:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> Response:
        return self._request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> Response:
        return self._request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs) -> Response:
        return self._request("DELETE", path, **kwargs)

    # ------------------------------------------------------------------
    # Internal request handler
    # ------------------------------------------------------------------

    def _request(self, method: str, path: str, **kwargs) -> Response:
        url = f"{self.base_url}{path}"

        timeout = kwargs.pop("timeout", self.timeout)

        self.logger.debug(
            f"➡️ {method} {url} | params={kwargs.get('params')} | json={kwargs.get('json')}"
        )

        start = time.time()
        response = self.session.request(
            method=method,
            url=url,
            timeout=timeout,
            **kwargs,
        )
        elapsed = time.time() - start

        self.logger.info(
            f"⬅️ {method} {url} | status={response.status_code} | {elapsed:.2f}s"
        )

        if self.logger.isEnabledFor(10):  # DEBUG
            try:
                self.logger.debug(f"Response body: {response.text}")
            except Exception:
                self.logger.debug("Response body could not be read")

        return response
