from users import *
from questions import *
from menus import *
from env import *
import sqlite3
from db import initialize_database, get_db_connection

def main():
    initialize_database()
    import_questions_from_csv(csv_file_path)
    print("Database initialized.")
    while True:
        logged_in_user_id = login_menu()
        if logged_in_user_id:
            user_main_menu(logged_in_user_id)
        else:
            break  # user chose to exit

if __name__ == "__main__":
    main()