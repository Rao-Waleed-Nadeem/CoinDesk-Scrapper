from http_client.client import HTTPClient

from api_clients.coindesk_client import CoinDeskClient

from parsers.homepage_parser import HomepageParser
from parsers.article_parser import ArticleParser


class CoinDeskScraper:

    BASE_URL = "https://www.coindesk.com"

    def __init__(self):

        self.http = HTTPClient()

        self.client = CoinDeskClient(http_client=self.http)

    def scrape_homepage(self):

        response = self.http.get(self.BASE_URL)

        if response is None:
            return []

        return HomepageParser.parse(response.text)

    def scrape_timeline(
        self,
        size=16,
        pagination=None,
    ):

        return self.client.timeline(
            size=size,
            pagination=pagination,
        )

    def scrape_article(self, article_url):

        response = self.http.get(article_url)

        if response is None:
            return None

        return ArticleParser.parse(response.text)

    def enrich_article(self, article):

        if not article.url:
            return article

        detail = self.scrape_article(article.url)

        if detail is None:
            return article

        article.body = detail.body

        article.tags = detail.tags

        article.author = detail.author

        article.image_url = detail.image_url

        return article

    def enrich_articles(self, articles):

        enriched = []

        for article in articles:

            enriched.append(self.enrich_article(article))

        return enriched

    def close(self):

        self.http.close()
