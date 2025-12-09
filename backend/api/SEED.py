import mysql.connector
import random
import time
def get_connection():
    return mysql.connector.connect(
    host= "127.0.0.1",
    port= 3305,
    database= "flight_game",
    user= "root",
    password= "tishchuk6370",
    autocommit = True
)

def quiz_questions(limit = 5):
    conn = get_connection()
    cur = conn.cursor()
    query = "Select question, choice_a, choice_b, choice_c, choice_d, correct_choice FROM quiz ORDER BY RAND() LIMIT %s"
    cur.execute(query, (limit,))
    results = cur.fetchall()
    cur.close()
    conn.close()
    questions_list = []
    for row in results:
        questions_list.append({
            "question": row[0],
            "choices": {
                "A": row[1],
                "B": row[2],
                "C": row[3],
                "D": row[4]
            },
            "correct_choice": row[5]
        })
    return questions_list

def initialize_quiz_table(force=False):
    conn = get_connection()
    cur = conn.cursor() 
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS quiz (
                id INT AUTO_INCREMENT PRIMARY KEY,
                question TEXT NOT NULL,
                choice_a VARCHAR(255),
                choice_b VARCHAR(255),
                choice_c VARCHAR(255),
                choice_d VARCHAR(255),
                correct_choice CHAR(1)
            )
        """)
        conn.commit()
        cur.execute("SELECT COUNT(*) FROM quiz")
        count = cur.fetchone()[0]
        if count >= 40 and not force:
            return f"Quiz table already has {count} rows; skipping insert."
        if force:
            cur.execute("TRUNCATE TABLE quiz")
            conn.commit()

        insert_sql = """
            INSERT INTO quiz (question, choice_a, choice_b, choice_c, choice_d, correct_choice)
            VALUES (%s,%s,%s,%s,%s,%s)
        """
        cur.executemany(insert_sql, questions)
        conn.commit()
        return f"Successfully inserted {len(questions)} questions into quiz table."
    finally:
        try:
            cur.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass

def check_answer(correct_choice, user_choice):
    return correct_choice.upper() == user_choice.upper()


def initialize_player_table():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS player (
                Player_Name VARCHAR(50) PRIMARY KEY,
                Easy_Score INT(11) NULL DEFAULT NULL,
	            Medium_Score INT(11) NULL DEFAULT NULL,
	            Hard_Score INT(11) NULL DEFAULT NULL
            )
        """)
        conn.commit()
        return "Player table initialized successfully."
    finally:
        try:
            cur.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass

