from users import *
from questions import *
from db import initialize_database, get_db_connection

def login_menu():
    while True:
        logged_in_user_id = None 
        print("Welcome to Bear Down!")
        print("1. Login to existing user")
        print("2. Create New User")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            user_id = login(username, password)
            if user_id:
                logged_in_user_id = user_id
                print(f"Welcome back, {username}!")
                return logged_in_user_id
            else:
                print("Invalid username or password.")
        elif choice == '2':
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            try:
                create_user(username, password)
                print("User created successfully!")
            except Exception as e:
                print(f"Error creating user: {e}")
        elif choice == '3':
            print("Goodbye!")
            return None
        else:
            print("Invalid choice. Please try again.")