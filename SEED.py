import mysql.connector
import random
import time
questions = [  # (question, choice_a, choice_b, choice_c, choice_d, correct_choice)
        ("Who is credited with the first powered, controlled, sustained flight?", "Wright brothers", "Alberto Santos-Dumont", "Otto Lilienthal", "Samuel Langley", "A"),
        ("What year did the Wright brothers achieve their first flight?", "1899", "1903", "1914", "1927", "B"),
        ("What does 'FAA' stand for in the United States?", "Flight and Aviation Agency", "Federal Aviation Administration", "Federal Air Authority", "Flight Assessment Agency", "B"),
        ("What is the primary lift-generating surface on an airplane?", "Fuselage", "Wing", "Rudder", "Aileron", "B"),
        ("Which instrument shows aircraft altitude?", "Airspeed indicator", "Altimeter", "Attitude indicator", "Variometer", "B"),
        ("What force opposes lift and pulls the aircraft down?", "Thrust", "Drag", "Gravity", "Lift", "C"),
        ("What do thrust and drag primarily affect?", "Lift", "Weight", "Forward motion", "Yaw", "C"),
        ("Which control changes roll about the longitudinal axis?", "Rudder", "Elevator", "Aileron", "Flaps", "C"),
        ("What part of the airplane is used to control yaw?", "Aileron", "Rudder", "Elevator", "Spoiler", "B"),
        ("Which famous transatlantic solo flight was completed by Charles Lindbergh?", "Spirit of St. Louis", "Enola Gay", "The Red Baron", "Flyer II", "A"),
        ("What does ICAO stand for?", "International Civil Aviation Organization", "International Council of Air Operators", "Intercontinental Aviation Organization", "Institute for Civil Aviation Oversight", "A"),
        ("What is a black box on aircraft?", "GPS device", "Flight data recorder", "Cockpit voice amplifier", "Autopilot unit", "B"),
        ("Which aircraft completed the first non-stop transatlantic flight in 1919?", "Vickers Vimy", "Spirit of St. Louis", "Wright Flyer", "Boeing 247", "A"),
        ("What is the main purpose of flaps?", "Increase cruise speed", "Improve braking", "Increase lift at low speeds", "Control yaw", "C"),
        ("Which engine type is most common on modern airliners?", "Piston engine", "Turboprop", "Turbofan", "Ramjet", "C"),
        ("What does 'VFR' stand for?", "Visual Flight Rules", "Variable Flight Regulations", "Visual Fuel Response", "Vehicle Flight Route", "A"),
        ("What does 'IFR' stand for?", "Instrument Flight Rules", "International Flight Regulations", "Integrated Flight Route", "International Fuel Rules", "A"),
        ("Which wing shape is typical for high-speed aircraft?", "Delta", "Straight", "Elliptical", "Gull", "A"),
        ("What is the term for the front section of an aircraft?", "Empennage", "Fuselage", "Nacelle", "Canopy", "B"),
        ("What year did Boeing 747 first fly?", "1966", "1970", "1958", "1980", "A"),
        ("Which aircraft dropped the atomic bomb on Hiroshima?", "Enola Gay", "Spirit of St. Louis", "Memphis Belle", "Bockscar", "A"),
        ("What is the name of the tail assembly?", "Cockpit", "Empennage", "Fuselage", "Nacelle", "B"),
        ("What is indicated airspeed?", "True wind speed", "Speed relative to the air", "Ground speed", "Mach number", "B"),
        ("Which airport is commonly known as LHR?", "Los Angeles International", "London Heathrow", "Lagos Airport", "Lima Airport", "B"),
        ("What does 'METAR' provide?", "Aircraft maintenance logs", "Pilot training schedule", "Routine aviation weather report", "Air traffic clearances", "C"),
        ("Who flew the first solo non-stop flight around the world?", "Charles Lindbergh", "Jerrie Mock", "Amelia Earhart", "Howard Hughes", "B"),
        ("Which control surface increases lift for takeoff and landing?", "Rudder", "Elevator", "Flaps", "Trim tab", "C"),
        ("What does 'ATC' stand for?", "Air Traffic Control", "Airline Transport Certificate", "Aviation Training Center", "Airline Technical Crew", "A"),
        ("What is Mach 1?", "One kilometer per hour", "One nautical mile per hour", "Speed of sound", "Twice the speed of sound", "C"),
        ("Which aviator disappeared over the Pacific in 1937?", "Charles Lindbergh", "Amelia Earhart", "Orville Wright", "Howard Hughes", "B"),
        ("Which device measures engine thrust on jets?", "Altimeter", "Tachometer", "Thrust meter (EPR/N1)", "Airspeed indicator", "C"),
        ("What is the wingtip device that reduces drag?", "Spoiler", "Flap", "Winglet", "Rudder", "C"),
        ("Which material is commonly used for modern airliner fuselages?", "Wood", "Aluminum alloys and composites", "Iron", "Titanium only", "B"),
        ("What is a stall in aerodynamics?", "Engine failure", "Loss of lift due to high angle of attack", "Tire burst", "Over-speeding", "B"),
        ("What does 'GPS' mean?", "Global Positioning System", "Ground Positioning Service", "General Pilot System", "Global Plane Service", "A"),
        ("Which country produced the Concorde?", "USA", "France/UK", "Germany", "Japan", "B"),
        ("What is the primary purpose of an altimeter?", "Measure airspeed", "Measure altitude", "Measure fuel", "Measure engine temperature", "B"),
        ("Which instrument shows aircraft attitude relative to horizon?", "Altimeter", "Turn coordinator", "Attitude indicator", "Airspeed indicator", "C"),
        ("What is the name for small movable surfaces on the trailing edge used for roll control?", "Rudder", "Ailerons", "Flaps", "Slats", "B"),
        ("Which historical plane dropped the first operational jet bomber bomb?", "Heinkel He 178", "Me 262", "Avro Vulcan", "None of the above", "B"),
        ("What is the standard sea level pressure used in aviation (hPa)?", "1013.25", "1000.00", "980.00", "1025.00", "A"),
        ("Which organization is responsible for global aviation safety standards?", "NASA", "ICAO", "FAA only", "IATA", "B"),
        ("What is the main fixed surface that supports the fuselage and engines?", "Wing", "Tail", "Aileron", "Rudder", "A"),
        ("Which British aviator made the first nonstop flight from England to Australia (1928)?", "Charles Kingsford Smith", "Amy Johnson", "Howard Hughes", "Bessie Coleman", "A"),
        ("What is a black box primarily used for?", "Entertainment system", "Flight data and voice recording", "Fuel monitoring", "Autopilot backup", "B"),
        ("What wing device increases lift at very low speeds mostly during takeoff?", "Slats", "Rudder", "Spoiler", "Aileron", "A"),
        ("Which instrument indicates the rate of climb or descent?", "Turn coordinator", "Vertical speed indicator", "Altimeter", "Airspeed indicator", "B")
    ]

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
    import random
    return random.sample(questions, limit)

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


def generate_random_weather(delay):
    sql = "SELECT name FROM goal"
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    weathers = [row[0] for row in result]
    needed_weathers = {'CLEAR', 'CLOUDS', 'WINDY'}
    filtered_weathers = [w for w in weathers if w.upper() in needed_weathers]
    if filtered_weathers:
        random_weather = random.choice(filtered_weathers).lower().capitalize()
    else:
        random_weather = random.choice(['Clear', 'Clouds', 'Windy'])
    time.sleep(delay)
    return random_weather

def get_random_airports_from_finland(limits=3):
    sql = f" SELECT airport.name , airport.iata_code FROM airport INNER JOIN country ON airport.iso_country = country.iso_country WHERE country.name = 'Finland' AND airport.iata_code != '' AND airport.iata_code != 'HEL' ORDER BY RAND() LIMIT {limits}"
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    for name, iata in result:
        print(f"🛫 {iata} - {name}")
    return ''


def get_start_airport():
    sql = "SELECT name FROM airport WHERE latitude_deg = 60.3172 AND longitude_deg = 24.963301"
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result:
        return result[0]
    return "Helsinki Vantaa Airport"


def get_helsinki_vantaa_coords():
    sql = "SELECT latitude_deg, longitude_deg , name FROM airport WHERE name = 'Helsinki Vantaa Airport'"
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result:
        return result
    return (60.3172, 24.963301, "Helsinki Vantaa Airport")

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