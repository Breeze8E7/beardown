import sqlite3

def get_db_connection():
    return sqlite3.connect('masterdatabase.db')

def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE,
        password TEXT
    )
    ''')

    # Create progress table (chapter access)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        course TEXT NOT NULL,
        chapter TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    # Create questions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course TEXT,
        chapter TEXT,
        question TEXT,
        answer TEXT,
        option_a TEXT,
        option_b TEXT,
        option_c TEXT,
        option_d TEXT
    )
    ''')

    # Create question_progress table (mastery tracking)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS question_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        correct_attempts INTEGER DEFAULT 0,
        total_attempts INTEGER DEFAULT 0,
        consecutive_correct INTEGER DEFAULT 0,
        mastered BOOLEAN DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (question_id) REFERENCES questions(id),
        UNIQUE(user_id, question_id)
    )
    ''')

    conn.commit()
    conn.close()
