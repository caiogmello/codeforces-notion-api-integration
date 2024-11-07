import datetime


class PropertyFormatter:
    def __init__(self):
        self._colors = ["blue", "brown", "default", "gray", "green", "pink", "orange", "purple", "red", "yellow"]
        self._tag_colors = {}

    def format_submission(self, submission: dict) -> dict:
        return {
            "Id": self._format_id(submission["id"]),
            "ContestId": self._format_contest_id(submission["contestId"]),
            "Name": self._format_name(submission["name"]),
            "Index": self._format_index(submission["index"]),
            "Rating": self._format_rating(submission["rating"]),
            "Tags": self._format_tags(submission["tags"]),
            "Time": self._format_time(submission["time"]),
            "URL": self._format_url(submission["url"]),
        }

    def _format_id(self, id: int) -> dict:
        return {
            "type": "title",
            "title": [{"type": "text", "text": {"content": str(id)}}],
        }

    def _format_contest_id(self, contest_id: int) -> dict:
        return {
            "type": "rich_text",
            "rich_text": [{"type": "text", "text": {"content": str(contest_id)}}],
        }

    def _format_name(self, name: str) -> dict:
        return {"type": "rich_text", "rich_text": [{"type": "text", "text": {"content": name}}]}

    def _format_index(self, index: str) -> dict:
        return {
            "type": "rich_text",
            "rich_text": [{"type": "text", "text": {"content": index}}],
        }

    def _format_rating(self, rating: int) -> dict:
        return {"type": "number", "number": rating}

    def _format_multi_select(self, tag: str):
        return {"name": tag, "color": self._get_tag_color(tag)}

    def _format_tags(self, tags: list) -> dict:
        return {
            "type": "multi_select",
            "multi_select": [self.format_multi_select(tag) for tag in tags],
        }

    def _format_time(self, time: str):
        return {
            "type": "date",
            "date": {
                "start": datetime.datetime.strptime(
                    time, "%d/%m/%Y %H:%M:%S"
                ).isoformat(),
                "end": None,
            },
        }

    def _format_url(self, url: str) -> dict:
        return {"type": "url", "url": url}
    
    def _get_tag_color(self, tag: str) -> str:
        if tag not in self._tag_colors:
            self._tag_colors[tag] = self._get_color(tag)
        return self._tag_colors[tag]

    def _get_color(self, tag) -> str:
        return self._colors[hash(tag) % len(self._colors)]

