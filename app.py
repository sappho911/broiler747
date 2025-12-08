from flask import Flask, jsonify
import mysql.connector
import requests
import random
from flask import request
from SEED import (
    quiz_questions, 
    check_answer,  
    get_selected_airport,
    initialize_quiz_table
)
from flask_cors import CORS
## fix the def get_connection since its not fully working 
def get_connection():
    return mysql.connector.connect(
    host= "127.0.0.1",
    port= 3305,
    database= "flight_game",
    user= "root",
    password= "tishchuk6370",
    autocommit = True
    )
app = Flask(__name__)
CORS(app)

@app.route("/api/players", methods=["GET"])
def playersfetcher():
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT screen_name FROM game"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    # Convert list of tuples into JSON objects
    players = [{"name": row[0]} for row in results]
    return jsonify(players)

@app.route("/api/<name>", methods=["GET"]) 
def namefetcher(name): ## Fetch data from the database depending the name given in the URL parameter.
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT name FROM goal WHERE name = %s"
    cursor.execute(query, (name,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"goals": results}

@app.route("/start", methods=["POST"])
def start(): 
    data = request.json
    player_name = data.get("name") if data else None
    
    if not player_name:
        return {"error": "Player name is required"}, 400
    
    try:
        initialize_quiz_table()
        start_airport = get_start_airport()
        helsinki_coords = get_helsinki_vantaa_coords()
        weather = generate_random_weather(0)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM goal WHERE name = %s", (player_name,))
        existing_goal = cursor.fetchone()
        
        if not existing_goal:
            cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM goal")
            next_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO goal (id, name) VALUES (%s, %s)", (next_id, player_name))
            conn.commit()
            message = "New game created successfully"
        else:
            message = "Game started successfully"
        
        cursor.close()
        conn.close()
        
        return {
            "message": message,
            "player": player_name,
            "starting_airport": start_airport,
            "coordinates": {
                "latitude": helsinki_coords[0],
                "longitude": helsinki_coords[1]
            },
            "weather": weather,
            "fuel": 100,
            "score": 0
        }
    except Exception as e:
        return {"error": str(e)}, 500
  

@app.route('/refuel', methods=['POST'])
def refuel():
    refueled = random.choice([True, False])
    return {"refueled": refueled}

@app.route("/seed_quiz", methods=["GET"])
def seed_quiz(): 
    return {"questions": quiz_questions(5)}

@app.route("/anwers", methods=["POST"])
def Asnwers():
    data = request.json
    correct_choice = data.get("correct_choice")
    user_choice = data.get("user_choice")
    if not correct_choice or not user_choice:
        return {"error": "Missing correct_choice or user_choice"}
  
    is_correct = check_answer(correct_choice, user_choice)
    
    return {
        "correct": is_correct,
        "correct_choice": correct_choice,
        "user_choice": user_choice
    }
@app.route("/saveresult", methods=["POST"])
def save_result():
   """ data = request.json
    name = data.get("name")
    score = data.get("score")
    
    if not name or score is None:
        return {"error": "Missing name or score"}, 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM goal WHERE name = %s", (name,))
        player = cursor.fetchone()
        
        if not player:
            cursor.close()
            conn.close()
            return {"error": f"Player '{name}' not found"}, 404
        cursor.execute("UPDATE goal SET description = %s WHERE name = %s", (f"Score: {score}", name))
        conn.commit()
        cursor.close()
        conn.close()
        
        return {"message": "Result saved successfully", "name": name, "score": score}
    except Exception as e:
        return {"error": str(e)}, 500"""
   return {"message": "Functionality not implemented yet and i need someone to ask about it"} 


@app.route("/airports", methods=["get"])
def get_airports():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT airport.name, airport.iata_code, airport.latitude_deg, airport.longitude_deg
            FROM airport 
            INNER JOIN country ON airport.iso_country = country.iso_country 
            WHERE country.name = 'Finland' 
            AND airport.iata_code != '' 
            AND airport.iata_code != 'HEL' 
            ORDER BY RAND() 
            LIMIT 5
        """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        airports = [
            {
                "name": row[0], 
                "iata_code": row[1],
                "latitude": float(row[2]),
                "longitude": float(row[3])
            } 
            for row in results
        ]
        
        return {"airports": airports}
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/destination", methods=["POST"])
def get_destination():
    data = request.json
    iata_code = data.get("iata_code")
    if not iata_code:
        return {"error": "IATA code is required"}, 400
    try:
        airport_info = get_selected_airport(iata_code)
        
        if not airport_info:
            return {"error": f"Airport with IATA code '{iata_code}' not found"}, 404
        
        return {
            "name": airport_info[0],
            "latitude": airport_info[1],
            "longitude": airport_info[2],
            "iata_code": iata_code
        }
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/weather", methods=["get"])
def get_weather():
    """Get random weather conditions"""
    try:
        weather = generate_random_weather(0)
        return {"weather": weather}
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")