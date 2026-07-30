"""
Authentication strategies for API clients.
"""

from typing import Dict


class Authentication:
    """Base authentication strategy."""

    def apply(self, headers: Dict[str, str]) -> Dict[str, str]:
        return headers


class BearerTokenAuth(Authentication):

    def __init__(self, token: str):
        self.token = token

    def apply(self, headers):

        headers["Authorization"] = f"Bearer {self.token}"

        return headers


class APIKeyAuth(Authentication):

    def __init__(self, api_key: str, header_name: str = "X-API-Key"):
        self.api_key = api_key
        self.header_name = header_name

    def apply(self, headers):

        headers[self.header_name] = self.api_key

        return headers
