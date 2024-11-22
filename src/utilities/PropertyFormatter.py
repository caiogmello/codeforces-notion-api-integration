import datetime
import json
import os

script_dir = os.path.dirname(os.path.abspath(os.path.join(__file__, "../../")))
json_dir = os.path.join(script_dir, "src", "json")

class PropertyFormatter:
    def __init__(self):
        """
        Class to format the properties of the submissions to be posted in the Notion database.
        """

        self._colors = [
            "blue",
            "brown",
            "default",
            "gray",
            "green",
            "pink",
            "orange",
            "purple",
            "red",
            "yellow",
        ]
        self._tag_colors = {}
        self._db_info = None

    def set_db_data(self) -> None:
        """
        Set the database information from the JSON file to avoid coloring tag errors.
        """
        with open(
            os.path.join(json_dir, "notion_db_info.json"), "r", encoding="utf8"
        ) as f:
            self._db_info = json.load(f)
        self._set_all_tag_colors()

    def format_submission(self, submission: dict) -> dict:
        return {
            "Name": self._format_name(submission["name"], submission["url"]),
            "Rating": self._format_rating(submission["rating"]),
            "Tags": self._format_tags(submission["tags"]),
            "Time": self._format_time(submission["time"]),
            "ContestId": self._format_contest_id(submission["contestId"]),
            "Index": self._format_index(submission["index"]),
            "Id": self._format_id(submission["id"]),
        }

    def get_db_properties(self) -> dict:
        return {
            "Name": {
                "rich_text": {},
            },
            "Rating": {
                "number": {},
            },
            "Tags": {
                "multi_select": {},
            },
            "Time": {
                "date": {},
            },
            "ContestId": {
                "rich_text": {},
            },
            "Index": {
                "rich_text": {},
            },
            "Id": {
                "title": {},
            },
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

    def _format_name(self, name: str, url: str) -> dict:
        return {
            "type": "rich_text",
            "rich_text": [
                {
                    "type": "text",
                    "text": {"content": name, "link": {"url": url}},
                    "annotations": {"color": "blue", "underline": True},
                }
            ],
        }

    def _format_index(self, index: str) -> dict:
        return {
            "type": "rich_text",
            "rich_text": [{"type": "text", "text": {"content": index}}],
        }

    def _format_rating(self, rating: int) -> dict:
        return {"type": "number", "number": rating}

    def _format_time(self, time: str):
        local_time = datetime.datetime.strptime(time, "%d/%m/%Y %H:%M:%S")
        local_timezone = datetime.datetime.now().astimezone().tzinfo
        local_time = local_time.replace(tzinfo=local_timezone)
        return {
            "type": "date",
            "date": {
                "start": local_time.isoformat(),
                "end": None,
            },
        }

    def _format_multi_select(self, tag: str):
        return {"name": tag, "color": self._get_tag_color(tag)}

    def _format_tags(self, tags: list) -> dict:
        return {
            "type": "multi_select",
            "multi_select": [self._format_multi_select(tag) for tag in tags],
        }

    def _get_tag_color(self, tag: str) -> str:
        if tag not in self._tag_colors:
            self._tag_colors[tag] = self._get_color(tag)
        return self._tag_colors[tag]

    def _get_color(self, tag) -> str:
        return self._colors[hash(tag) % len(self._colors)]

    def _set_all_tag_colors(self):
        for tag in self._db_info["properties"]["Tags"]["multi_select"]["options"]:
            self._tag_colors[tag["name"]] = tag["color"]

        return self._tag_colors
