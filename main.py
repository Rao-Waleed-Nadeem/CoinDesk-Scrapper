from scrapers.coindesk_html import scrape_homepage
from scrapers.downloader import download_pdf


def main():

    print("=" * 50)
    print("CoinDesk Scraper Started")
    print("=" * 50)

    articles = scrape_homepage()

    print("\nLatest Headlines\n")

    for article in articles[:10]:
        print(article["title"])

    download_pdf()

    print("\nFinished Successfully!")


if __name__ == "__main__":
    main()
