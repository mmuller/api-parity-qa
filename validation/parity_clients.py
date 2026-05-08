# parity_clients

import requests
from validation.config import BASE_URL


class BaseClient:
    def __init__(self, default_headers=None):
        self.default_headers = default_headers or {}

    def _merge_headers(self, headers):
        return {**self.default_headers, **(headers or {})}

    def get(self, path, headers=None):
        return requests.get(
            f"{BASE_URL}{path}",
            headers=self._merge_headers(headers),
        )

    def post(self, path, payload, headers=None):
        return requests.post(
            f"{BASE_URL}{path}",
            json=payload,
            headers=self._merge_headers(headers),
        )


class ClientOG(BaseClient):
    """Original system (no bugs)"""

    pass


class ClientNG(BaseClient):
    """New system (can simulate bugs)"""

    def __init__(self, bug_mode=None):
        headers = {}
        if bug_mode:
            headers["x-bug-mode"] = bug_mode
        super().__init__(default_headers=headers)
