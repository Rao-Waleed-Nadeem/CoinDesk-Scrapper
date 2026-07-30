"""
Pagination helper classes.
"""


class CursorPagination:

    def __init__(self):

        self.last_id = None
        self.last_display_date = None

    def update(self, article):

        self.last_id = article.get("id")

        self.last_display_date = article.get("displayDate")

    def params(self):

        params = {}

        if self.last_id:

            params["lastId"] = self.last_id

        if self.last_display_date:

            params["lastDisplayDate"] = self.last_display_date

        return params
