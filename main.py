from src.db_updater import DBupdater
from dotenv import load_dotenv
import os


if __name__ == '__main__':
    if (load_dotenv()):
        notion_token = os.getenv('NOTION_TOKEN')
        db_id = os.getenv('DATABASE_ID_TESTE')
        user_handle = os.getenv('CF_HANDLE')

        db_updater = DBupdater(notion_token, db_id, user_handle)
        db_updater.update_db()
