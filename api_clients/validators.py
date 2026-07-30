"""
Response validation helpers.
"""

from .exceptions import (
    InvalidJSONError,
    UnexpectedContentTypeError,
    ValidationError,
)


class ResponseValidator:

    @staticmethod
    def validate_json_response(response):

        content_type = response.headers.get("Content-Type", "")

        if "application/json" not in content_type:

            raise UnexpectedContentTypeError(
                f"Expected JSON, received '{content_type}'"
            )

        try:

            return response.json()

        except Exception as e:

            raise InvalidJSONError(str(e))

    @staticmethod
    def require_keys(data, required_keys):

        missing = [key for key in required_keys if key not in data]

        if missing:

            raise ValidationError(f"Missing required keys: {', '.join(missing)}")

        return True
