from bs4 import BeautifulSoup

from http_client.client import HTTPClient

client = HTTPClient()

response = client.get("https://www.coindesk.com/")

if response:

    soup = BeautifulSoup(response.text, "html.parser")

    titles = soup.find_all("h2")

    print("\nLatest Headlines\n")

    for title in titles[:10]:

        text = title.get_text(strip=True)

        if text:

            print(text)

client.close()
