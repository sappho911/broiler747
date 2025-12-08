from flask import Flask, jsonify
import mysql.connector
import requests
import random
from flask import request
from SEED import (
    quiz_questions, 
    check_answer, 
    initialize_quiz_table,
    Select_weather,
    end_country
)
from flask_cors import CORS
#fix the def get_connection since its not fully working
def get_connection():
    return mysql.connector.connect(
    host= "127.0.0.1",
    port= 3306,
    database= "flight_game",
    user= "root",
    password= "KissaKoira",
    autocommit = True
    )

app = Flask(__name__)
CORS(app)
@app.route("/api/<name>", methods=["GET"]) 
def namefetcher(name): ## Fetch data from the database depending the name given in the URL parameter.

    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM goal WHERE name = %s"
    cursor.execute(query, (name,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()


    return {"goals": results}



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
def airports():
    try:
        airports = get_selected_airport()
        return {"airports": airports}
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/end',methods=['POST'])
def end():
    data = request.json
    airport_identifier = data.get("name") if data else None
    player_name = data.get("player_name") if data else None

    if not airport_identifier:
        return {"error": "Airport name/code is required"}, 400

    try:
        airport_data = end_country(airport_identifier, player_name)
        if not airport_data:
            return {"error": f"Airport '{airport_identifier}' not found"}, 404
        return {"airport": airport_data, "player_name": player_name}
    except Exception as e:
        return {"error": str(e)}, 500

if __name__== '__main__':
    app.run(debug=True)