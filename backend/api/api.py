# api file adding code soon
import random
from api.SEED  import quiz_questions, initialize_quiz_table, get_connection
from model.airport import Select_weather
from flask import jsonify, request

def register_routes(app):
    @app.route("/weather", methods=["POST"])
    def takerequest():
        data = request.json
        weather = data.get("weather") if data else None
        name = data.get("name") if data else None
        
        if not weather or not name:
            return {"error": "Weather choice and name are required"}, 400
     
        try:
            message = Select_weather(weather)
            return {"message": message , "name": name}
        except Exception as e:
            return {"error": str(e)}, 500 

    @app.route("/seed_quiz", methods=["GET"])
    def seed_quiz(): 
        return {"questions": quiz_questions(5)}


    @app.route('/refuel', methods=['POST'])
    def refuel():
        refueled = random.choice([True, False])
        return {"refueled": refueled}

    @app.route("/api/players", methods=["GET"])
    def playersfetcher():
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT Player_Name FROM player"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        # Convert list of tuples into JSON objects
        players = [{"name": row[0]} for row in results]
        return jsonify(players)    
    @app.route("/api/players/stats", methods=["GET"])
    def playerstats():
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT Player_Name, Easy_Score, Medium_Score, Hard_Score FROM player"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        stats = [{"name": row[0], "easy_score": row[1], "medium_score": row[2], "hard_score": row[3]} for row in results]
        return jsonify(stats)

    @app.route('/api/<name>', methods=['GET'])
    def userfetcher(name):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
            user = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if user:
                return {
                    "id": user[0],
                    "name": user[1],
                    "score": user[2]
                }
            else:
                return {"error": "User not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500


    @app.route("/start_game", methods=["POST"])
    def start_game():
        data = request.json
        name = data.get("name") if data else None
        
        if not name:
            return {"error": "Name is required"}, 400
        
        try:
            initialize_quiz_table(name)
            return {"message": f"Game started for {name}"}
        except Exception as e:
            return {"error": str(e)}, 500
    
    @app.route('/ending_airport', methods= ["POST"])

## player post name,other nulls at the start 
    @app.route('/new_player', methods=['POST'])
    def new_player():
        data = request.json
        name = data.get("name") 
        if not data or 'name' not in data: 
            return {'error': 'Name is required'}, 400
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO player (Player_Name) VALUES (%s)', (request.json['name'],))
        conn.commit()
        cursor.close()
        conn.close()
        return {'message': 'New player added successfully'}, 201
        
    @app.route('/score', methods= ["POST"])
    def scores():
        data = request.json
        score = data.get("score") if data else None
        if not score:
            return {"error": "Score is required"}, 400
        else:
            return {"score": score}
    return app
