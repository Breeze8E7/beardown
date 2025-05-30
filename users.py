import sqlite3
from db import get_db_connection

def create_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT INTO users (username, password)
        VALUES (?, ?)
        ''', (username, password))
        conn.commit()
        print(f"User '{username}' created.")
    except sqlite3.IntegrityError:
        print(f"Username already exists.")
    finally:
        conn.close()

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

import sqlite3
from db import get_db_connection

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
                INSERT INTO user_question_bank (user_id, question_id)
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
    conn.close()
    for chapter in chapters:
        unlock_chapter(user_id, course, chapter)
    print(f"Course '{course}' unlocked for user ID {user_id}.")
