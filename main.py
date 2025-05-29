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
    logged_in_user_id = login_menu()
    if logged_in_user_id is None:
        print("Exiting the application.")
        return
    print(f"User {logged_in_user_id} logged in successfully. Test successfully created.")
    return

if __name__ == "__main__":
    main()