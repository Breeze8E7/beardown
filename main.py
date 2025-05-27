from users import *
from questions import *
import sqlite3
from db import initialize_database, get_db_connection


def main():
    initialize_database()
    print("Database initialized.")
    logged_in_user_id = None 

    while True:
        print("\nChoose an option:")
        print("1. Create New User")
        print("2. Login")
        if logged_in_user_id:
            print("3. Add Question")
            print("4. Logout")
            print("5. Exit")
        else:
            print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            username = input("Username: ").strip()
            email = input("Email (optional): ").strip() or None
            password = input("Password (optional): ").strip() or None
            try:
                create_user(username, email, password)
            except Exception as e:
                print(f"Error creating user: {e}")

        elif choice == '2':
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            user_id = login(username, password)
            if user_id:
                logged_in_user_id = user_id
                print(f"Welcome back, {username}!")
            else:
                print("Invalid username or password.")

        elif choice == '3':
            if logged_in_user_id:
                # Add question flow only if logged in
                course = input("Course: ").strip()
                chapter = input("Chapter: ").strip()
                question = input("Question text: ").strip()
                answer = input("Answer: ").strip()
                option_a = input("Option A: ").strip()
                option_b = input("Option B: ").strip()
                option_c = input("Option C (optional): ").strip() or None
                option_d = input("Option D (optional): ").strip() or None
                link = input("Link (optional): ").strip() or None
                try:
                    add_question(course, chapter, question, answer, option_a, option_b, option_c, option_d)
                except Exception as e:
                    print(f"Error adding question: {e}")
            else:
                # If not logged in, option 3 is exit
                print("Goodbye!")
                break

        elif choice == '4' and logged_in_user_id:
            # Logout option
            logged_in_user_id = None
            print("Logged out successfully.")

        elif choice == '5' and logged_in_user_id:
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()