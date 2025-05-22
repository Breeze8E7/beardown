import sqlite3

def get_db_connection():
    return sqlite3.connect('questions.db')

def initialize_user_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE,
        password TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        course TEXT NOT NULL,
        chapter TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    conn.commit()
    conn.close()

def create_user(username, email=None, password=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT INTO users (username, email, password)
        VALUES (?, ?, ?)
        ''', (username, email, password))
        conn.commit()
        print(f"User '{username}' created.")
    except sqlite3.IntegrityError:
        print(f"Username or email already exists.")
    finally:
        conn.close()
        print(f"User '{username}' created.")

def login(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT id FROM users WHERE username = ? AND password = ?
    ''', (username, password))
    
    result = cursor.fetchone()
    conn.close()

    if result:
        user_id = result[0]
        print(f"Login successful. User ID: {user_id}")
        return user_id
    else:
        print("Login failed.")
        return None

def unlock_chapter(user_id, course, chapter):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT id FROM questions WHERE course = ? AND chapter = ?
    ''', (course, chapter))
    question_ids = [row[0] for row in cursor.fetchall()]
    for qid in question_ids:
        try:
            cursor.execute('''
            INSERT INTO question_progress (user_id, question_id)
            VALUES (?, ?)
            ''', (user_id, qid))
        except sqlite3.IntegrityError:
            continue
    conn.commit()
    conn.close()
    print(f"Chapter '{chapter}' unlocked for user ID {user_id} in course '{course}'.")

def unlock_course(user_id, course):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT DISTINCT chapter FROM questions WHERE course = ?
    ''', (course,))
    chapters = [row[0] for row in cursor.fetchall()]
    for chapter in chapters:
        unlock_chapter(user_id, course, chapter)
    conn.close()
    print(f"Course '{course}' unlocked for user ID {user_id}.")