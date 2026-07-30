from models.article import Article


class TimelineParser:

    @staticmethod
    def parse(article_data: dict) -> Article:

        return Article(
            id=article_data.get("id", ""),
            title=article_data.get("title", ""),
            slug=article_data.get("slug", ""),
            url=article_data.get("url"),
            description=article_data.get("description"),
            image_url=article_data.get("image", {}).get("url"),
            display_date=article_data.get("displayDate"),
            published_at=article_data.get("publishedAt"),
        )

    @classmethod
    def parse_many(cls, articles):

        return [cls.parse(article) for article in articles]
