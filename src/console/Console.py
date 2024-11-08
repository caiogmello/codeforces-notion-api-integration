class Console:
    def __init__(self):
        pass

    def greetings(self):
        self.dots()
        print("Welcome to the Codeforces Notion Updater!")
        print(
            f"This script will update a Notion database with your Codeforces submissions."
        )
        print(
            f"Please make sure you have your {self.bold('Notion Integration Token')} and the {self.bold('Page ID')} ready."
        )
        print(
            "You can find more information on how to obtain them in the README file. "
        )
        self.dots()
        print()

    def get_user_input(self):
        notion_token = self.get_notion_token()
        page_id = self.get_database_url()
        user_handle = self.get_user_handle()

        return notion_token, page_id, user_handle

    def get_database_url(self):
        page_id = input(self.bold("Enter your Notion Page URL: "))
        print()
        return page_id

    def get_user_handle(self):
        user_handle = input(self.bold("Enter the Codeforces username: "))
        print()
        return user_handle

    def get_notion_token(self):
        notion_token = input(self.bold("Enter your Notion Integration Token: "))
        print()
        return notion_token

    def take_a_while(self):
        print("This may take a while depending on the number of submissions.")
        print("Please wait...\n")

    def welcome_back(self):
        self.dots()
        print("Welcome back!")
        print(
            "Let's update your Notion database with your latest public Codeforces submissions."
        )
        self.dots()
        print()

    def select_option(self, db_name):
        self.dots("_", 40)
        print(self.bold("SELECT AN OPTION:"))
        print(self.bold(self.red(f"1. Update {db_name}'s Notion database")))
        print(f"{self.bold('2.')} Change Codeforces username")
        print(f"{self.bold('3.')} Exit")
        option = input("ANS: ")
        self.dots("_", 40)

        print()

        return option

    def new_database(self):
        print("Creating a new Notion Database...")

    def ok(self):
        print(self.bold("OK.\n"))

    def submissions_added(self,  url, number):
        if number == 1:
            print(self.green(f"Database {url} updated successfully with new {number} problem. \n"))
            return
        elif number < 1:
            print(self.green("No new submissions to update. \n"))
            return

        print(self.green(f"Database {url} updated successfully with new {number} problems. \n"))


    def exit(self):
        print("\nGoodbye.")

    def updated(self, text):
        r = f"The {text} was updated successfully.\n"
        print(self.bold(r))

    def bold(self, text):
        return f"\033[1m{text}\033[0m"

    def green(self, text):
        return f"\033[92m{text}\033[0m"

    def red(self, text):
        return f"\033[91m{text}\033[0m"

    def dots(self, text=".", number=80):
        print(self.red(text) * number)
