import sqlite3
import csv
from db import get_db_connection

def add_question(course, chapter, question, answer, option_a, option_b, option_c = None, option_d = None, link = None):
    if not course or not chapter or not question or not answer or not option_a or not option_b:
        raise ValueError("All fields are required.")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO questions (course, chapter, question, answer, option_a, option_b, option_c, option_d, link)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (course, chapter, question, answer, option_a, option_b, option_c, option_d, link))
    conn.commit()
    conn.close()
    print(f"Question added successfully to {course} - {chapter}.")

def import_questions_from_csv(file_path):
    conn = get_db_connection()
    cursor = conn.cursor()
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            course = row['course']
            chapter = row['chapter']
            question = row['question']
            answer = row['answer']
            option_a = row['option_a']
            option_b = row['option_b']
            option_c = row.get('option_c') or None
            option_d = row.get('option_d') or None
            link = row.get('link') or None

            cursor.execute('''
            INSERT INTO questions (course, chapter, question, answer, option_a, option_b, option_c, option_d, link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (course, chapter, question, answer, option_a, option_b, option_c, option_d, link))

    conn.commit()
    conn.close()
    print("CSV questions imported successfully.")

from db import get_db_connection

def handle_correct_answer(user_id, question_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Update progress for a correct answer
    cursor.execute('''
        UPDATE user_question_bank
        SET
            total_attempts = total_attempts + 1,
            correct_attempts = correct_attempts + 1,
            consecutive_correct = consecutive_correct + 1
        WHERE user_id = ? AND question_id = ?
    ''', (user_id, question_id))

    # Check if consecutive_correct now qualifies for mastery
    cursor.execute('''
        SELECT consecutive_correct FROM user_question_bank
        WHERE user_id = ? AND question_id = ?
    ''', (user_id, question_id))
    consecutive_correct = cursor.fetchone()[0]

    if consecutive_correct >= 3:
        cursor.execute('''
            UPDATE user_question_bank
            SET mastered = TRUE
            WHERE user_id = ? AND question_id = ?
        ''', (user_id, question_id))

    conn.commit()
    conn.close()

def handle_incorrect_answer(user_id, question_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Update progress for an incorrect answer
    cursor.execute('''
        UPDATE user_question_bank
        SET
            total_attempts = total_attempts + 1,
            consecutive_correct = 0,
            mastered = FALSE
        WHERE user_id = ? AND question_id = ?
    ''', (user_id, question_id))

    conn.commit()
    conn.close()
