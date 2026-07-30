from parsers.timeline_parser import TimelineParser
from api_clients.base_api_client import BaseAPIClient


class CoinDeskClient(BaseAPIClient):

    def __init__(self, http_client=None):

        super().__init__(
            base_url="https://www.coindesk.com/api/v1", http_client=http_client
        )

    def timeline(
        self, size=16, last_id=None, last_display_date=None, lang="en", pagination=None
    ):

        params = {
            "size": size,
            "lang": lang,
        }

        if pagination:

            params.update(pagination.params())
        if last_id:
            params["lastId"] = last_id

        if last_display_date:
            params["lastDisplayDate"] = last_display_date

        data = self.get(
            "/articles/timeline",
            params=params,
        )

        articles = TimelineParser.parse_many(data["articles"])

        if pagination and articles:

            last = data["articles"][-1]

            pagination.update(last)

        return articles
