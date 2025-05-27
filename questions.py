import sqlite3
from db import get_db_connection

def add_question(course, chapter, question, answer, option_a, option_b, option_c = None, option_d = None):
    if not course or not chapter or not question or not answer or not option_a or not option_b:
        raise ValueError("All fields are required.")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO questions (course, chapter, question, answer, option_a, option_b, option_c, option_d)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (course, chapter, question, answer, option_a, option_b, option_c, option_d))
    conn.commit()
    conn.close()
    print(f"Question added successfully to {course} - {chapter}.")