import json
import requests
import os
try:
    from src.property_formatter import PropertyFormatter
except:
    from property_formatter import PropertyFormatter

class NotionAPI:
    def __init__(self, token, page_id):

        self._header = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2021-05-13",
        }

        self._TOKEN = token
        self._PAGE_ID = page_id	
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

        with open(os.path.join("src/json/", 'notion_db.json'), 'w', encoding='utf8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        
        return results

    def get_database_info(self):
        url = f"https://api.notion.com/v1/databases/{self._DATABASE_ID}"
        response = requests.get(url, headers=self._header)

        if response.status_code != 200:
            raise Exception(f"Request failed: {response.json()['message']}")
        else:
            with open(os.path.join("src/json/", 'notion_db_info.json'), 'w', encoding='utf8') as f:
                json.dump(response.json(), f, ensure_ascii=False, indent=4)
            
            self._formatter.set_db_data()

            return response.json()

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
        
    def create_database(self, title: str = "CF problems"):
        url = "https://api.notion.com/v1/databases"

        payload = {
            "icon": {
                "type": "emoji",
                "emoji": "🪖"
            },
            "parent": {
                "type": "page_id",
                "page_id": self._PAGE_ID
            },
            "title": [
                {
                    "type": "text",
                    "text": {
                        "content": title
                    }
                }
            ],
            "properties": self._formatter.get_db_properties()
        }

        
        response = requests.post(url, headers=self._header, data=json.dumps(payload))
        if response.status_code != 200:
            raise Exception(f"Request failed: {response.json()['message']}")
        else:
            file_name = f'{"_".join(title.lower().split(" "))}_notion_db_info.json'
            with open(os.path.join("src/json/", file_name), 'w', encoding='utf8') as f:
                json.dump(response.json(), f, ensure_ascii=False, indent=4)
            return response.json()
        
    def delete_page(self, page_id: str):
        url = f"https://api.notion.com/v1/pages/{page_id}"

        payload = {"archived": True}
        
        response = requests.patch(url, json=payload, headers=self._header)
        if response.status_code != 200:
            raise Exception(f"Request failed: {response.json()['message']}")
        else:
            return response.json()
    

        
