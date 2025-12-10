import mysql.connector
import random
import time
def get_connection():
    return mysql.connector.connect(
    host= "127.0.0.1",
    port= 3306,
    database= "flight_game",
    user= "root",
    password= "2004",
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

