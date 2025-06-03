import sqlite3
import random
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

def display_user_progress(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            q.course,
            q.chapter,
            COUNT(*) AS total_questions,
            SUM(CASE WHEN uqb.mastered = 1 THEN 1 ELSE 0 END) AS mastered_questions
        FROM user_question_bank uqb
        JOIN questions q ON uqb.question_id = q.id
        WHERE uqb.user_id = ?
        GROUP BY q.course, q.chapter
        ORDER BY q.course, q.chapter
    ''', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        print("No questions unlocked yet.")
        return
    print("\nYour Progress Overview:")
    for course, chapter, total, mastered in rows:
        print(f"Course: {course} | Chapter: {chapter} | Mastered: {mastered}/{total}")

import random
from db import get_db_connection

def generate_quiz(user_id, num_questions=10):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Step 1: Get unmastered questions
    cursor.execute('''
        SELECT q.id, q.course, q.chapter, q.question, q.option_a, q.option_b, q.option_c, q.option_d, q.answer
        FROM questions q
        JOIN user_question_bank uqb ON q.id = uqb.question_id
        WHERE uqb.user_id = ? AND uqb.mastered = FALSE
    ''', (user_id,))
    unmastered = cursor.fetchall()

    # Step 2: If not enough, get mastered ones too
    if len(unmastered) < num_questions:
        cursor.execute('''
            SELECT q.id, q.course, q.chapter, q.question, q.option_a, q.option_b, q.option_c, q.option_d, q.answer
            FROM questions q
            JOIN user_question_bank uqb ON q.id = uqb.question_id
            WHERE uqb.user_id = ? AND uqb.mastered = TRUE
        ''', (user_id,))
        mastered = cursor.fetchall()

        if mastered:
            print("Insufficient unmastered questions; filling in with previously mastered questions.")

        total_pool = unmastered + mastered
    else:
        total_pool = unmastered

    if not total_pool:
        print("No questions available in your bank.")
        conn.close()
        return []

    selected = random.sample(total_pool, min(num_questions, len(total_pool)))
    conn.close()
    return selected