from tqdm import tqdm
from datetime import datetime
from src.api.CodeforcesAPI import CodeforcesAPI
from src.api.NotionAPI import NotionAPI
from src.console.Console import Console


class DbUpdater:
    def __init__(self, notion_token, page_id, db_id, user_handle):
        self._cf_api = CodeforcesAPI()
        self._notion_api = NotionAPI(notion_token, page_id)
        self._db_id = db_id
        self._user_handle = user_handle
        self._notion_api.set_database_id(db_id)
        self._db_data = None
        self._cf_submissions = None
        self._db_info = self._notion_api.get_database_info()


    def update_db(self) -> None:
        print(f"Getting {self._user_handle} public Codeforces submissions...")
        submissions = self._cf_api.get_submissions(self._user_handle)
        self._cf_submissions = self._cf_api.format_all_submissions(submissions)
        self._db_data = self._notion_api.get_pages(1)
        Console().ok()

        print(f"Updating Notion '{self._db_info['title'][0]['text']['content']}' database...")
        if (len(self._db_data) == 0) or len(self._db_data[0]['properties']['Name']['rich_text']) == 0:
            for submission in tqdm(self._cf_submissions):
                self._notion_api.create_page(submission)
            Console().ok()
            Console().submissions_added(self._db_info['url'], len(self._cf_submissions))
            return
        
        i = 0
        object_datetime = datetime.strptime(self._cf_submissions[i]['time'], '%d/%m/%Y %H:%M:%S').replace(tzinfo=datetime.now().astimezone().tzinfo)
        last_db_datetime = datetime.strptime(self._db_data[0]['properties']['Time']['date']['start'], '%Y-%m-%dT%H:%M:%S.%f%z')
        while object_datetime > last_db_datetime:
            i += 1
            object_datetime = datetime.strptime(self._cf_submissions[i]['time'], '%d/%m/%Y %H:%M:%S').replace(tzinfo=datetime.now().astimezone().tzinfo)
        
        if i == 1:
            Console().ok()
            Console().submissions_added(self._db_info['url'], 0)
            return
        
        for j in tqdm(range(i-1)):
            self._notion_api.create_page(self._cf_submissions[j])
        
        Console().ok()
        Console().submissions_added(self._db_info['url'], i-1)





    