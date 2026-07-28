from .base_parser import BaseParser
from .utils import (
    extract_attr,
    extract_text,
    normalize_url,
)


class HomepageParser(BaseParser):
    """
    Parse the CoinDesk homepage.

    Returns:
        List of article dictionaries.
    """

    # -------------------------
    # CSS Selectors
    # -------------------------

    ARTICLE_SELECTOR = "article"

    TITLE_SELECTOR = "h2"

    LINK_SELECTOR = "a"

    CATEGORY_SELECTOR = '[data-testid="eyebrow"]'

    IMAGE_SELECTOR = "img"

    # -------------------------
    # Main Parser
    # -------------------------

    def parse(self):
        """
        Parse homepage articles.
        """

        articles = []

        cards = self.select_all(self.ARTICLE_SELECTOR)

        for card in cards:

            article = self.parse_article(card)

            if article:
                articles.append(article)

        return articles

    # -------------------------
    # Individual Article Parser
    # -------------------------

    def parse_article(self, card):
        """
        Parse a single homepage article.
        """

        title = extract_text(card.select_one(self.TITLE_SELECTOR))

        url = normalize_url(
            extract_attr(
                card.select_one(self.LINK_SELECTOR),
                "href",
            )
        )

        category = extract_text(card.select_one(self.CATEGORY_SELECTOR))

        image = normalize_url(
            extract_attr(
                card.select_one(self.IMAGE_SELECTOR),
                "src",
            )
        )

        article = {
            "title": title,
            "url": url,
            "category": category,
            "image": image,
        }

        try:

            self.validate(
                article,
                [
                    "title",
                    "url",
                ],
            )

        except ValueError:

            return None

        return article
