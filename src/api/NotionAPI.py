import json
import requests
import os
from src.utilities.PropertyFormatter import PropertyFormatter
from src.utilities.ExceptionHandler import ExceptionHandler


class NotionAPI:

    def __init__(self, token: str, page_id: str) -> "NotionAPI":
        """
        Class to interact with the Notion API and get the database information and post the new submissions.

        - token: API token for Notion API
        - page_id: ID of the page where the database is/will be located
        """
        self._header = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2021-05-13",
        }

        self._TOKEN: str = token
        self._PAGE_ID: str = page_id
        self._DATABASE_ID: str = None
        self._formatter = PropertyFormatter()

    def get_pages(self, num_pages: int = None) -> list:
        """
        Get all 'num_pages' pages from the database,
        or get all pages if 'num_pages' is None.
        """

        if self._DATABASE_ID is None:
            raise ExceptionHandler("Database ID not set")

        url = f"https://api.notion.com/v1/databases/{self._DATABASE_ID}/query"

        get_all = num_pages is None
        page_size = 100 if get_all else num_pages

        payload = {
            "page_size": page_size,
            "sorts": [{"property": "Time", "direction": "descending"}],
        }

        response = requests.post(url, headers=self._header, data=json.dumps(payload))

        if response.status_code != 200:
            raise ExceptionHandler(response.json()["message"])

        data = response.json()
        results = data["results"]

        while data["has_more"] and get_all:
            payload = {
                "page_size": page_size,
                "start_cursor": data["next_cursor"],
                "sorts": [{"property": "Time", "direction": "descending"}],
            }

            url = f"https://api.notion.com/v1/databases/{self._DATABASE_ID}/query"
            response = requests.post(url, json=payload, headers=self._header)
            data = response.json()
            results.extend(data["results"])

        with open(
            os.path.join("src/json/", "notion_db.json"), "w", encoding="utf8"
        ) as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

        return results

    def get_database_info(self) -> dict:
        """
        Get information about the database. Like the title, properties, etc.
        """

        url = f"https://api.notion.com/v1/databases/{self._DATABASE_ID}"
        response = requests.get(url, headers=self._header)

        if response.status_code != 200:
            raise ExceptionHandler(response.json()["message"])

        with open(
            os.path.join("src/json/", "notion_db_info.json"), "w", encoding="utf8"
        ) as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)

        self._formatter.set_db_data()

        return response.json()

    def get_page_info(self) -> dict:
        """
        Get information about the page. Like the title, properties, etc.
        """

        url = f"https://api.notion.com/v1/pages/{self._PAGE_ID}"
        response = requests.get(url, headers=self._header)

        if response.status_code != 200:
            raise ExceptionHandler(response.json()["message"])

        with open(
            os.path.join("src/json/", "notion_page_info.json"), "w", encoding="utf8"
        ) as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)

        return response.json

    def set_database_id(self, database_id: str) -> None:
        self._DATABASE_ID = database_id

    def create_page(self, data: dict) -> dict:
        """
        Create a new page in the database. All rows in a Notion Database are pages with specific properties.
        So, this function creates a new row in the database.
        """

        url = "https://api.notion.com/v1/pages"

        payload = {
            "parent": {"database_id": self._DATABASE_ID},
            "properties": self._formatter.format_submission(data),
        }

        response = requests.post(url, headers=self._header, data=json.dumps(payload))

        if response.status_code != 200:
            raise ExceptionHandler(response.json()["message"])

        return response.json()

    def create_database(self, title: str = "CF problems") -> dict:
        """
        Create a new database in the parent page.
        You may create a new database for a new user.
        """
        url = "https://api.notion.com/v1/databases"

        payload = {
            "icon": {"type": "emoji", "emoji": "🪖"},
            "parent": {"type": "page_id", "page_id": self._PAGE_ID},
            "title": [{"type": "text", "text": {"content": title}}],
            "properties": self._formatter.get_db_properties(),
        }

        response = requests.post(url, headers=self._header, data=json.dumps(payload))
        if response.status_code != 200:
            raise ExceptionHandler(response.json()["message"])

        file_name = f'{"_".join(title.lower().split(" "))}_notion_db_info.json'
        with open(os.path.join("src/json/", file_name), "w", encoding="utf8") as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)
        return response.json()
