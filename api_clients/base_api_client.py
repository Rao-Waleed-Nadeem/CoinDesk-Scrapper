"""
Reusable base class for REST API clients.
"""

import logging

from http_client.client import HTTPClient

from .auth import Authentication
from .validators import ResponseValidator


from http_client.client import HTTPClient
from .auth import Authentication
from .validators import ResponseValidator

import logging


class BaseAPIClient:

    def __init__(
        self,
        base_url,
        http_client=None,
        auth=None,
    ):

        self.base_url = base_url.rstrip("/")

        self.http = http_client or HTTPClient()

        self.auth = auth or Authentication()

        self.default_headers = {
            "Accept": "application/json",
        }

    def build_url(self, endpoint: str) -> str:

        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def build_headers(self, headers=None):

        final_headers = self.default_headers.copy()

        if headers:
            final_headers.update(headers)

        return self.auth.apply(final_headers)

    def get(
        self,
        endpoint,
        params=None,
        headers=None,
    ):

        url = self.build_url(endpoint)

        logging.info(f"API GET {url}")

        response = self.http.get(
            url,
            params=params,
            headers=self.build_headers(headers),
        )

        if response is None:

            raise ConnectionError("HTTP request failed.")

        return ResponseValidator.validate_json_response(response)

    def close(self):

        self.http.close()
