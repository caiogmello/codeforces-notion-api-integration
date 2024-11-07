import json
import requests
from property_formatter import PropertyFormatter
import os

class NotionAPI:
    def __init__(self, token):

        self._header = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2021-05-13",
        }

        self._TOKEN = token
        self._DATABASE_ID = None
        self._formatter = PropertyFormatter()

    def get_pages(self, num_pages: int):
        if self._DATABASE_ID is None:
            raise Exception("Database ID not set")

        url = f"https://api.notion.com/v1/databases/{self._DATABASE_ID}/query"

        payload = {"page_size": num_pages,
                   "sorts": [{
                          "property": "Time",
                          "direction": "descending"          
                            }],
                    }

        response = requests.post(url, headers=self._header, data=json.dumps(payload))


        if response.status_code != 200:
            raise Exception(f"Request failed: {response.json()['message']}")
        
        data = response.json()
        results = data["results"]

        while data["has_more"] and len(results) < num_pages:
            payload = {"page_size": num_pages, "start_cursor": data["next_cursor"]}
            url = f"https://api.notion.com/v1/databases/{self._DATABASE_ID}/query"
            response = requests.post(url, json=payload, headers=self._header)
            data = response.json()
            results.extend(data["results"])

        with open(os.path.join("./json/", 'notion_db.json'), 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        return results

    def set_database_id(self, database_id: str):
        self._DATABASE_ID = database_id

    def create_page(self, data: dict):
        url = "https://api.notion.com/v1/pages"

        payload = {"parent": {"database_id": self._DATABASE_ID}, "properties": self._formatter.format_submission(data)}

        response = requests.post(url, headers=self._header, data=json.dumps(payload))

        if response.status_code != 200:
            raise Exception(f"Request failed: {response.json()['message']}")
        else:
            return response.json()
        
    def delete_page(self, page_id: str):
        url = f"https://api.notion.com/v1/pages/{page_id}"

        payload = {"archived": True}
        
        response = requests.patch(url, json=payload, headers=self._header)
        if response.status_code != 200:
            raise Exception(f"Request failed: {response.json()['message']}")
        else:
            return response.json()
    

        
