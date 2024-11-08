from dotenv import load_dotenv
from src.console import Console
import os

class EnvManager:
    def __init__(self):
        self._notion_token = None
        self._db_id = None
        self._user_handle = None
        self._console = Console()
    
    def set_db_id(self, url: str) -> str:
        self._db_id = url.split("?")[0].split("/")[-1]
        self._console.updated("database ID")

    def set_user_handle(self, handle: str) -> str:
        self._user_handle =  handle
        self._console.updated("Codeforces handle")
    
    def set_notion_token(self, token: str) -> str:
        self._notion_token = token
        self._console.updated("Notion integration token")
    
    def write_env(self) -> None:
        with open('.env', 'w') as f:
            f.write(f"NOTION_TOKEN={self._notion_token}\n")
            f.write(f"DATABASE_ID={self._db_id}\n")
            f.write(f"CF_HANDLE={self._user_handle}\n")

    def load_env(self) -> bool:
        load_dotenv()    
        try:
            self._notion_token = os.getenv("NOTION_TOKEN")
            self._db_id = os.getenv("DATABASE_ID")
            self._user_handle = os.getenv("CF_HANDLE")
        except:
            pass

        return load_dotenv() and (self._notion_token is not None and self._db_id is not None and self._user_handle is not None)
    

        