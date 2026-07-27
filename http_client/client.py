import logging
import requests

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


class HTTPClient:

    def __init__(self):

        self.session = requests.Session()

        self.timeout = 15

        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Accept": "text/html,application/json",
            }
        )

        retry = Retry(
            total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504]
        )

        adapter = HTTPAdapter(max_retries=retry)

        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def get(self, url, **kwargs):

        try:

            logging.info(f"GET {url}")

            response = self.session.get(url, timeout=self.timeout, **kwargs)

            response.raise_for_status()

            return response

        except Exception as e:

            logging.error(e)

            return None

    def download(self, url, path):

        response = self.get(url, stream=True)

        if response is None:
            return

        with open(path, "wb") as file:

            for chunk in response.iter_content(8192):

                if chunk:
                    file.write(chunk)

        print("Download Finished")

    def close(self):

        self.session.close()
