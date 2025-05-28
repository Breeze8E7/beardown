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
            lesson_link = row.get('lesson_link') or None  # If you're using that new column

            cursor.execute('''
            INSERT INTO questions (course, chapter, question, answer, option_a, option_b, option_c, option_d, lesson_link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (course, chapter, question, answer, option_a, option_b, option_c, option_d, lesson_link))

    conn.commit()
    conn.close()
    print("CSV questions imported successfully.")