# api file adding code soon
import random
from api.SEED import quiz_questions
from model.airport import Select_weather, get_started_country
from flask import jsonify, request
from model.game import Game
from model.player import Player 
from model.airport import Airport, get_connection

def register_routes(app):
    @app.route("/airports", methods=["GET"])
    def get_airports():
        try:
            airports = get_started_country()
            return jsonify({"airports": airports})
        except Exception as e:
            return {"error": str(e)}, 500
    
    @app.route("/random_airports", methods=["GET"])
    def get_random_airports():
        try:
            limit = request.args.get("limit", 3, type=int)
            airport = Airport("EFHK")  
            airports = airport.get_random_airports_from_finland(limit)
            return jsonify({"airports": airports})
        except Exception as e:
            return {"error": str(e)}, 500
    
    # Calculate distance between two airports
    @app.route("/distance", methods=["POST"])
    def calculate_distance():
        data = request.json
        start_airport = data.get("start_airport") if data else None
        ending_airport = data.get("ending_airport") if data else None
        
        if not start_airport or not ending_airport:
            return {"error": "Both start_airport and ending_airport are required"}, 400
        
        try:
            game = Game("temp", start_airport, ending_airport, "sunny", 0)
            distance_data = game.distance(start_airport, ending_airport)
            km = distance_data.get("km", 0)
            difficulty = game.get_difficulty(km)
            return jsonify({"km": km, "difficulty": difficulty})
        except Exception as e:
            return {"error": str(e)}, 500
    
    @app.route("/save_game", methods=["POST"])
    def save_game():
        data = request.json
        player_name = data.get("player_name") if data else None
        start_airport = data.get("start_airport") if data else None
        ending_airport = data.get("ending_airport") if data else None
        weather = data.get("weather") if data else None
        
        if not all([player_name, start_airport, ending_airport, weather]):
            return {"error": "player_name, start_airport, ending_airport, and weather are required"}, 400
        
        try:
            game = Game(player_name, start_airport, ending_airport, weather, 0)
            distance_data = game.distance(start_airport, ending_airport)
            km = distance_data.get("km", 0)
            difficulty = game.get_difficulty(km)
            
            game.distancee = km
            game.difficulty = difficulty
            success = game.save_game_state()
            if success:
                return {"message": "Game saved successfully", "km": km, "difficulty": difficulty}
            else:
                return {"error": "Failed to save game"}, 500
        except Exception as e:
            return {"error": str(e)}, 500
    
    @app.route("/player_status", methods=["POST"])
    def player_status():
        data = request.json
        player_name = data.get("player_name") if data else None
        easy_score = data.get("easy_score", 0) if data else 0
        medium_score = data.get("medium_score", 0) if data else 0
        hard_score = data.get("hard_score", 0) if data else 0
        
        if not player_name:
            return {"error": "player_name is required"}, 400
        
        try:
            player = Player(player_name, easy_score, medium_score, hard_score)
            return jsonify(player.get_status())
        except Exception as e:
            return {"error": str(e)}, 500
    
    @app.route("/update_score", methods=["POST"])
    def update_player_score():
        data = request.json
        player_name = data.get("player_name") if data else None
        points = data.get("points", 0) if data else 0
        difficulty = data.get("difficulty") if data else None
        
        if not player_name:
            return {"error": "player_name is required"}, 400
        
        try:
            player = Player(player_name, 0, 0, 0)
            player.update_score(points)
            if difficulty:
                player.game_diff(difficulty)
            return jsonify(player.get_status())
        except Exception as e:
            return {"error": str(e)}, 500

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
    @app.route("/start_game", methods=["POST"])
    def start_game():
        data = request.json
        name = data.get("name") if data else None
        
        if not name:
            return {"error": "Name is required"}, 400
        
        try:
            return {"message": f"Game started for {name}"}
        except Exception as e:
            return {"error": str(e)}, 500
          
    @app.route("/api/players", methods=["GET"])
    def playersfetcher():
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT Player_Name FROM player"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
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

    @app.route('/ending_airport', methods= ["POST"])
    def ending_airport_choice():
        data = request.json
        ending_airport = data.get("ending_airport") if data else None
        if not ending_airport:
            return {"error": "Ending airport is required"}, 400
        return {"ending_airport": ending_airport}
    @app.route('/new_player', methods=['POST'])
    def new_player():
        data = request.json
        name = data.get("name") 
        if not data or 'name' not in data: 
            return {'error': 'Name is required'}, 400
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO player (Player_Name, Easy_Score, Medium_Score, Hard_Score) VALUES (%s, 0, 0, 0)', (request.json['name'],))
        conn.commit()
        cursor.close()
        conn.close()
        return {'message': 'New player added successfully'}, 201
    @app.route('/score', methods= ["POST"])
    def scores():
        data = request.json
        score = data.get("score") if data else None
        player_name = data.get("player_name") if data else None
        won = data.get("won", False) if data else False
        fuel_left = data.get("fuel_left", 0) if data else 0
        difficulty = data.get("difficulty") if data else None
        
        if score is None:
            return {"error": "Score is required"}, 400
        
        return jsonify({
            "success": True,
            "score": score,
            "player_name": player_name,
            "won": won,
            "fuel_left": fuel_left,
            "difficulty": difficulty,
            "message": "You won! Great flying!" if won else "Game over"
        })
      
    @app.route('/crashed', methods= ["POST"])
    def crashed():
        data = request.json
        crashed = data.get("crashed") if data else None
        player_name = data.get("player_name") if data else None
        fuel_left = data.get("fuel_left", 0) if data else 0
        distance_left = data.get("distance_left", 0) if data else 0
        difficulty = data.get("difficulty") if data else None
        score = data.get("score", 0) if data else 0
        
        if not crashed:
            return {"error": "Crashed status is required"}, 400
        
        return jsonify({
            "success": True,
            "crashed": crashed,
            "player_name": player_name,
            "fuel_left": fuel_left,
            "distance_left": distance_left,
            "difficulty": difficulty,
            "score": score,
            "message": "You crashed! Better luck next time."
        })
    
    @app.route('/update_final_score', methods=["POST"])
    def update_final_score():
        data = request.json
        player_name = data.get("player_name") if data else None
        difficulty = data.get("difficulty") if data else None
        score = data.get("score", 0) if data else 0
        
        if not player_name:
            return {"error": "player_name is required"}, 400
        if not difficulty:
            return {"error": "difficulty is required"}, 400
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            if difficulty == "easy":
                cursor.execute('SELECT Easy_Score FROM player WHERE Player_Name = %s', (player_name,))
            elif difficulty == "medium":
                cursor.execute('SELECT Medium_Score FROM player WHERE Player_Name = %s', (player_name,))
            elif difficulty == "hard":
                cursor.execute('SELECT Hard_Score FROM player WHERE Player_Name = %s', (player_name,))
            
            result = cursor.fetchone()
            current_score = result[0] if result else 0
            
            if score > current_score:
                if difficulty == "easy":
                    cursor.execute('UPDATE player SET Easy_Score = %s WHERE Player_Name = %s', (score, player_name))
                elif difficulty == "medium":
                    cursor.execute('UPDATE player SET Medium_Score = %s WHERE Player_Name = %s', (score, player_name))
                elif difficulty == "hard":
                    cursor.execute('UPDATE player SET Hard_Score = %s WHERE Player_Name = %s', (score, player_name))
                
                conn.commit()
                message = f"New high score! {score} points for {difficulty}"
                updated = True
            else:
                message = f"Score {score} not higher than current best {current_score}"
                updated = False
            
            cursor.close()
            conn.close()
            
            return jsonify({
                "success": True,
                "player_name": player_name,
                "difficulty": difficulty,
                "new_score": score,
                "previous_best": current_score,
                "updated": updated,
                "message": message
            })
        except Exception as e:
            print(f"Error updating final score: {e}")
            return {"error": str(e)}, 500      
   
        
    return app
