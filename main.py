from src.db_updater import DBupdater
from src.env_manager import EnvManager
from src.console import Console
from src.notion_api import NotionAPI
from dotenv import load_dotenv
import os


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
            console.new_database()
            db_info_json = notion_api.create_database(env._user_handle)
            
        env.set_db_id(db_info_json["id"])   
        env.write_env()
    

    current_user = os.getenv("CF_HANDLE")
    env.add_database_id(current_user, env._db_id) 

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
            dbs_ids = env.load_databases_ids()

            if current_user in dbs_ids:
                env.set_db_id(dbs_ids[current_user])
            else:
                db_name = console.new_database()
                new_db_info = notion_api.create_database(current_user)
                env.set_db_id(new_db_info["id"])

            env.set_user_handle(current_user)
            env.add_database_id(current_user, env._db_id)
            env.write_env()
        elif r == '3':
            console.exit()
            break
        else:
            print("Invalid option. Try again.")
            print()
        load_dotenv()

