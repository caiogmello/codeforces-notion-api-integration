from src.db_updater import DBupdater
from src.env_manager import EnvManager
from src.console import Console
from src.notion_api import NotionAPI
from dotenv import load_dotenv
import os
import json


if __name__ == '__main__':
    console = Console()
    env = EnvManager()

    if (env.load_env()):
        print("Loaded environment variables.")
        console.welcome_back()
    else:
        console.greetings()
        notion_token, page_id, user_handle = console.get_user_input()
        env.set_notion_token(notion_token)
        env.set_page_id(page_id)
        env.set_user_handle(user_handle)

        notion_api = NotionAPI(env._notion_token, env._page_id)
        db_info_json = None
        if os.getenv("DATABASE_ID") is None:
            db_name = console.create_database()
            db_info_json = notion_api.create_database(db_name)
            
        env.set_db_id(db_info_json["id"])   
        env.write_env()
    

    current_user = os.getenv("CF_HANDLE")

    while(True):
        r = console.select_option(current_user)
        notion_api = NotionAPI(env._notion_token, env._page_id)

        if r == '1':
            console.take_a_while()
            db_updater = DBupdater(env._notion_token, env._page_id, 
                                   env._db_id, env._user_handle)
            db_updater.update_db()
        elif r == '2':
            current_user = console.get_user_handle()
            db_name = console.new_database()
            new_db_info = notion_api.create_database(current_user)
            env.set_user_handle(current_user)
            env.set_db_id(new_db_info["id"])

            env.write_env()
        elif r == '3':
            console.exit()
            break
        else:
            print("Invalid option. Try again.")
            print()
        load_dotenv()

