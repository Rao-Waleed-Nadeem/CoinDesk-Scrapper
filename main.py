from scrapers.coindesk_scraper import CoinDeskScraper
from api_clients.pagination import CursorPagination

scraper = CoinDeskScraper()

pagination = CursorPagination()

articles = scraper.scrape_timeline(
    size=16,
    pagination=pagination,
)

articles = scraper.enrich_articles(articles)

for article in articles:

    print(article.title)

    print(article.author)

    print(article.url)

    print("-" * 80)

scraper.close()
