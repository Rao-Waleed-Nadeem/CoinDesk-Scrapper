from http_client.client import HTTPClient
from parsers.homepage_parser import HomepageParser


from pathlib import Path

from http_client.client import HTTPClient
from parsers.homepage_parser import HomepageParser

OUTPUT_DIR = Path("output")


def save_html(response_text: str):

    OUTPUT_DIR.mkdir(exist_ok=True)

    html_file = OUTPUT_DIR / "homepage.html"

    pretty_file = OUTPUT_DIR / "homepage_pretty.html"

    html_file.write_text(
        response_text,
        encoding="utf-8",
    )

    parser = HomepageParser(response_text)

    pretty_file.write_text(
        parser.soup.prettify(),
        encoding="utf-8",
    )


def scrape_homepage():

    client = HTTPClient()

    try:

        response = client.get("https://www.coindesk.com/")

        if response is None:
            return []

        save_html(response.text)

        parser = HomepageParser(response.text)

        articles = parser.parse()

        return articles

    finally:

        client.close()
