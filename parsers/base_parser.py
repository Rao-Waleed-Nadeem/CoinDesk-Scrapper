from abc import ABC, abstractmethod

from bs4 import BeautifulSoup

from .utils import (
    extract_attr,
    extract_list_text,
    extract_text,
    normalize_url,
    safe_select,
    safe_select_all,
    validate_required,
)


class BaseParser(ABC):
    """
    Base parser for all CoinDesk parsers.

    Every parser receives raw HTML and exposes
    a parse() method returning structured data.
    """

    def __init__(self, html: str):
        self.html = html
        self.soup = BeautifulSoup(html, "lxml")

    @abstractmethod
    def parse(self):
        """
        Must be implemented by child parsers.
        """
        pass

    # -------------------------
    # Helper Methods
    # -------------------------

    def select(self, selector: str):
        """
        Safe wrapper around select_one().
        """
        return safe_select(self.soup, selector)

    def select_all(self, selector: str):
        """
        Safe wrapper around select().
        """
        return safe_select_all(self.soup, selector)

    def get_text(self, selector: str):
        """
        Extract cleaned text using CSS selector.
        """
        return extract_text(self.select(selector))

    def get_attr(
        self,
        selector: str,
        attribute: str,
        normalize=False,
    ):
        """
        Extract HTML attribute safely.
        """

        value = extract_attr(
            self.select(selector),
            attribute,
        )

        if normalize:
            return normalize_url(value)

        return value

    def get_list_text(self, selector: str):
        """
        Extract multiple text values.

        Example:
            Tags
            Categories
        """
        return extract_list_text(self.select_all(selector))

    def validate(
        self,
        data: dict,
        required_fields: list[str],
    ):
        """
        Validate required parser fields.
        """

        if not validate_required(
            data,
            required_fields,
        ):
            missing = [field for field in required_fields if not data.get(field)]

            raise ValueError(f"Missing required fields: {missing}")

        return data
