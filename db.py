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
        password TEXT NOT NULL
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
        option_d TEXT,
        link TEXT
    )
    ''')
    # Create user_question_bank table with progress tracking embedded
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_question_bank (
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
    # Create indexes for performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_question ON user_question_bank(user_id, question_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_uqb_user ON user_question_bank(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_uqb_mastered ON user_question_bank(user_id, mastered)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_uqb_question ON user_question_bank(question_id)')
    conn.commit()
    conn.close()
