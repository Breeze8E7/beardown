from users import *
from questions import *
from db import initialize_database, get_db_connection

def login_menu():
    while True: 
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

def user_main_menu(logged_in_user_id):
    while True:
        print("The results of your last quiz are:")
        print("What would you like to do?")
        print("1. Take a Quiz.")
        print("2. Add chapter to quiz bank.")
        print("3. Add course to quiz bank.")
        print("4. View quiz bank.")
        print("5. Logout")
        print("6. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            # Take a quiz
            pass
        elif choice == '2':
            # Add chapter to quiz bank
            pass
        elif choice == '3':
            # Add course to quiz bank
            pass
        elif choice == '4':
            # View quiz bank
            pass
        elif choice == '5':
            print("Logging out...")
            return
        elif choice == '6':
            print("Exiting the application. Goodbye!")
            return
        else:
            print("Invalid choice. Please try again.")