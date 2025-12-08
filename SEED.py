import mysql.connector
import random
import time

def get_connection():
    return mysql.connector.connect(
    host= "127.0.0.1",
    port= 3306,
    database= "flight_game",
    user= "root",
    password= "KissaKoira",
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
    """Create player table if it doesn't exist"""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS player (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE,
                score INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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


def get_selected_airport(destination):
    sql = f"SELECT airport.name, airport.latitude_deg, airport.longitude_deg FROM airport WHERE iata_code ='{destination}'"
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result:
        return (result[0], float(result[1]), float(result[2]))
    return None


def Select_weather(Weather): ## this will save the  data to player database when the user choice their weather
    conn = get_connection()
    cur = conn.cursor()
    insert_sql = "INSERT INTO player (weather) VALUES (%s)"
    cur.execute(insert_sql, (Weather,))
    conn.commit()
    cur.close()
    return f"Weather choice '{Weather}' saved successfully."

def get_started_country():  ## this will select a country aka finland to start then it will  select  all of then send it
    conn = get_connection()
    cur = conn.cursor()
    query = """
        SELECT airport.name, airport.iata_code, airport.latitude_deg, airport.longitude_deg
        FROM airport 
        INNER JOIN country ON airport.iso_country = country.iso_country 
        WHERE country.name = 'Finland' 
        AND airport.iata_code != '' 
        AND airport.iata_code != 'HEL' 
        ORDER BY RAND()
    """
    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    return [
        {
            "name": row[0], 
            "iata_code": row[1],
            "latitude": float(row[2]),
            "longitude": float(row[3])
        } 
        for row in results
    ]

def saver():## this just saves and  the user choice of airport to database  
    conn = get_connection
    cur = conn.cursor()
    try:
        query = """
            INSERT INTO goal (name, description) 
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE description = %s
        """
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        if cur:
            cur.close()
        if conn:
            conn.close()
        print(f"Error saving airport choice: {e}")
        return False
    

def end_country(airport_identifier): ## User chooses their ending airport by name or IATA code
    conn = get_connection()
    cur = conn.cursor()
    query = """
        SELECT airport.name, airport.iata_code, airport.latitude_deg, airport.longitude_deg
        FROM airport 
        WHERE (airport.iata_code = %s OR airport.name = %s)
        AND airport.iata_code != ''
    """
    cur.execute(query, (airport_identifier, airport_identifier))
    result = cur.fetchone()
    cur.close()
    conn.close()
    if result:
        return {
            "name": result[0], 
            "iata_code": result[1],
            "latitude": float(result[2]),
            "longitude": float(result[3])
        }
    
    ## now we save his bs  to database by running the function above
    return None