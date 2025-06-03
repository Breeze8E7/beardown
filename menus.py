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
            take_a_quiz_menu(logged_in_user_id)
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

def take_a_quiz_menu(user_id):
    print("\n🧠 Starting a new quiz...\n")
    questions = generate_quiz(user_id, num_questions=10)
    if not questions:
        print("⚠️ No questions available in your bank. Unlock some chapters first.")
        return
    correct_count = 0
    incorrect_links = []
    for idx, q in enumerate(questions, 1):
        print(f"\nQuestion {idx}: {q['question']}")
        print(f"A. {q['option_a']}")
        print(f"B. {q['option_b']}")
        print(f"C. {q['option_c']}")
        print(f"D. {q['option_d']}")
        if q['link']:
            print(f"🔗 Link: {q['link']}")
        while True:
            answer = input("Your answer (A/B/C/D): ").strip().lower()
            if answer in ['a', 'b', 'c', 'd']:
                break
            print("Invalid input. Please enter A, B, C, or D.")
        correct_answer = q['answer'].strip().lower()
        if answer == correct_answer:
            handle_correct_answer(user_id, q['id'])
            correct_count += 1
        else:
            handle_incorrect_answer(user_id, q['id'])
            print(f"💡 Correct answer was: {q['answer']}")
            if q['link']:
                incorrect_links.append(q['link'])
    print(f"\n📊 Quiz complete! You got {correct_count}/{len(questions)} correct.")
    if incorrect_links:
        print("\n🔗 Review these links for questions you missed:")
        for link in incorrect_links:
            print(f"- {link}")
    while True:
        print("\nWhat would you like to do next?")
        print("1. Return to Main Menu")
        print("2. Exit")
        next_action = input("Enter your choice: ").strip()
        if next_action == '1':
            return  # Go back to user_main_menu
        elif next_action == '2':
            print("👋 Goodbye!")
            exit()
        else:
            print("Invalid choice. Please enter 1 or 2.")