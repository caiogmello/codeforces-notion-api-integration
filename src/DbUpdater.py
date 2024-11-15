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

        self._db_data = self._notion_api.get_pages()

        saved_submissions = set()
        for submission in self._db_data:
            saved_submissions.add(submission['properties']['Id']['title'][0]['text']['content'])

        Console().ok()

        print(f"Updating Notion '{self._db_info['title'][0]['text']['content']}' database...")
        i = 0


        new_submissions = []
        for submission in reversed(self._cf_submissions):
            if str(submission['id']) in saved_submissions:
                continue
            i += 1
            new_submissions.append(submission)

        if i > 0:
            for submission in tqdm(new_submissions):
                self._notion_api.create_page(submission)

        Console().ok()

        Console().submissions_added(self._db_info['url'], i)





    