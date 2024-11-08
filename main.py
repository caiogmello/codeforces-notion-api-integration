from src.db_updater import DBupdater
from src.env_manager import EnvManager
from src.console import Console


if __name__ == '__main__':
    console = Console()
    env = EnvManager()

    if (env.load_env()):
        print("Loaded environment variables.")
        console.welcome_back()
    else:
        console.greetings()
        notion_token, db_id, user_handle = console.get_user_input()
        env.set_notion_token(notion_token)
        env.set_db_id(db_id)
        env.set_user_handle(user_handle)
        env.write_env()

    while(True):
        r = console.select_option()

        if r == '1':
            console.take_a_while()
            db_updater = DBupdater(env._notion_token, env._db_id, env._user_handle)
            db_updater.update_db()
        elif r == '2':
            user_handle = console.get_user_handle()
            env.set_user_handle(user_handle)
            env.write_env()
        elif r == '3':
            db_id = console.get_database_url()
            env.set_db_id(db_id)
            env.write_env()
        elif r == '4':
            notion_token = console.get_notion_token()
            env.set_notion_token(notion_token)
            env.write_env()
        elif r == '5':
            console.exit()
            break
        else:
            print("Invalid option. Try again.")
            print()
