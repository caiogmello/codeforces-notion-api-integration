from src.codeforces_api import CodeforcesAPI
from src.notion_api import NotionAPI
import os
import json
from tqdm import tqdm
from datetime import datetime

class DBupdater:
    def __init__(self, notion_token, db_id, user_handle):
        self._cf_api = CodeforcesAPI()
        self._notion_api = NotionAPI(notion_token)
        self._db_id = db_id
        self._user_handle = user_handle
        self._notion_api.set_database_id(db_id)
        self._db_data = None
        self._cf_submissions = None


    def update_db(self) -> None:
        print(f"Getting {self._user_handle} Codeforces submissions...")
        submissions = self._cf_api.get_submissions(self._user_handle)
        self._cf_submissions = self._cf_api.format_all_submissions(submissions)

        self._db_data = self._notion_api.get_pages(300)

        print("Updating Notion database...")
        if (len(self._db_data) == 0) or len(self._db_data[0]['properties']['Name']['rich_text']) == 0:
            for submission in tqdm(self._cf_submissions):
                self._notion_api.create_page(submission)
        else:
            i = 0
            pbar = tqdm(total=len(self._cf_submissions))

            object_datetime = datetime.strptime(self._cf_submissions[i]['time'], '%d/%m/%Y %H:%M:%S').replace(tzinfo=datetime.now().astimezone().tzinfo)
            last_db_datetime = datetime.strptime(self._db_data[0]['properties']['Time']['date']['start'], '%Y-%m-%dT%H:%M:%S.%f%z')

            while object_datetime > last_db_datetime:
                if str(self._cf_submissions[i]['id']) != self._db_data[0]['properties']['Id']['title'][0]['text']['content']:
                    self._notion_api.create_page(self._cf_submissions[i])
                i += 1
                pbar.update(1)
                object_datetime = datetime.strptime(self._cf_submissions[i]['time'], '%d/%m/%Y %H:%M:%S').replace(tzinfo=datetime.now().astimezone().tzinfo)

            pbar.close()

        print("Database updated successfully.")





    