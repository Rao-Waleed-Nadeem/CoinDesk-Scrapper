def main():

    print("=" * 50)
    print("CoinDesk Scraper Started")
    print("=" * 50)

    from scrapers.coindesk_html import scrape_homepage
    from scrapers.downloader import download_pdf

    scrape_homepage()

    download_pdf()

    print("\nFinished Successfully!")


if __name__ == "__main__":
    main()
