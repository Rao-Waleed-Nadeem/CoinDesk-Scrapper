from http_client.client import HTTPClient

client = HTTPClient()

client.download(
    "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
    "downloads/sample.pdf",
)

client.close()
