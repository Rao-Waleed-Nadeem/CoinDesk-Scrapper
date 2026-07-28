from .base_parser import BaseParser
from .utils import (
    extract_attr,
    extract_list_text,
    extract_text,
    normalize_url,
)


class ArticleParser(BaseParser):
    """
    Parse a complete CoinDesk article page.
    """

    # ---------------------------------
    # CSS Selectors
    # ---------------------------------

    TITLE_SELECTOR = "h1"

    AUTHOR_SELECTOR = '[data-testid="author-name"]'

    DATE_SELECTOR = "time"

    BODY_SELECTOR = "article"

    PARAGRAPH_SELECTOR = "p"

    TAG_SELECTOR = 'a[href*="/tag/"]'

    IMAGE_SELECTOR = "img"

    DESCRIPTION_SELECTOR = 'meta[name="description"]'

    KEYWORDS_SELECTOR = 'meta[name="keywords"]'

    CANONICAL_SELECTOR = 'link[rel="canonical"]'

    # ---------------------------------
    # Main Parser
    # ---------------------------------

    def parse(self):
        """
        Parse the complete article.
        """

        article = {
            "title": self.get_title(),
            "author": self.get_author(),
            "published_at": self.get_publish_date(),
            "body": self.get_body(),
            "tags": self.get_tags(),
            "images": self.get_images(),
            "metadata": self.get_metadata(),
        }

        self.validate(
            article,
            [
                "title",
                "body",
            ],
        )

        return article

    # ---------------------------------
    # Individual Extraction Methods
    # ---------------------------------

    def get_title(self):

        return self.get_text(self.TITLE_SELECTOR)

    def get_author(self):

        return self.get_text(self.AUTHOR_SELECTOR)

    def get_publish_date(self):

        return self.get_attr(
            self.DATE_SELECTOR,
            "datetime",
        )

    def get_body(self):

        article = self.select(self.BODY_SELECTOR)

        if article is None:
            return None

        paragraphs = article.select(self.PARAGRAPH_SELECTOR)

        body = []

        for paragraph in paragraphs:

            text = extract_text(paragraph)

            if text:
                body.append(text)

        if not body:
            return None

        return "\n\n".join(body)

    def get_tags(self):

        return self.get_list_text(self.TAG_SELECTOR)

    def get_images(self):

        images = []

        for image in self.select_all(self.IMAGE_SELECTOR):

            src = normalize_url(
                extract_attr(
                    image,
                    "src",
                )
            )

            if src:
                images.append(src)

        return images

    def get_metadata(self):

        return {
            "description": self.get_attr(
                self.DESCRIPTION_SELECTOR,
                "content",
            ),
            "keywords": self.get_attr(
                self.KEYWORDS_SELECTOR,
                "content",
            ),
            "canonical": self.get_attr(
                self.CANONICAL_SELECTOR,
                "href",
                normalize=True,
            ),
        }
