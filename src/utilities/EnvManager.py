from dotenv import load_dotenv
from src.console.Console import Console
import os
import json


class EnvManager:
    def __init__(self):
        """
        Class to manage the environment variables and the databases IDs.
        """
        self._notion_token: str = None
        self._page_id: str = None
        self._db_id: str = None
        self._user_handle: str = None
        self._console = Console()

    def set_db_id(self, id: str) -> str:
        self._db_id = id

    def set_page_id(self, url: str) -> str:
        self._page_id = url.split("?")[0][-32:]

    def set_user_handle(self, handle: str) -> str:
        self._user_handle = handle

    def set_notion_token(self, token: str) -> str:
        self._notion_token = token

    def write_env(self) -> None:
        """
        Write the environment (NOTION_TOKEN, PAGE_ID, DATABASE_ID, CF_HANDLE) variables to the .env file.
        """
        with open(".env", "w") as f:
            f.write(f"NOTION_TOKEN={self._notion_token}\n")
            f.write(f"PAGE_ID={self._page_id}\n")
            f.write(f"DATABASE_ID={self._db_id}\n")
            f.write(f"CF_HANDLE={self._user_handle}\n")

    def load_env(self) -> bool:
        """
        Load the environment variables from the .env file.
        """

        load_dotenv()
        try:
            self._notion_token = os.getenv("NOTION_TOKEN")
            self._page_id = os.getenv("PAGE_ID")
            self._user_handle = os.getenv("CF_HANDLE")
            self._db_id = os.getenv("DATABASE_ID")
        except:
            pass

        return load_dotenv() and (
            self._notion_token is not None
            and self._page_id is not None
            and self._db_id is not None
            and self._user_handle is not None
        )

    def load_databases_ids(self) -> list:
        """
        Load the databases IDs from the databases_ids.json file.
        """

        db_ids = {"init": None}
        try:
            with open(os.path.join("src/json/", "databases_ids.json"), "r") as f:
                db_ids = json.load(f)
        except:
            with open(
                os.path.join("src/json/", "databases_ids.json"), "w", encoding="utf8"
            ) as f:
                json.dump(db_ids, f, ensure_ascii=False, indent=4)

        return db_ids

    def add_database_id(self, user_handle: str, db_id: str) -> None:
        """
        Add a new database ID to the databases_ids.json file.
        """

        db_ids = self.load_databases_ids()
        db_ids[user_handle] = db_id
        with open(
            os.path.join("src/json/", "databases_ids.json"), "w", encoding="utf8"
        ) as f:
            json.dump(db_ids, f, ensure_ascii=False, indent=4)
