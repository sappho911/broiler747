# api file adding code soon
import random
from api.SEED  import quiz_questions
from model.airport import Select_weather, get_started_country
from flask import jsonify, request
from model.game import Game
from model.player import Player 
from model.airport import Airport, get_connection

def register_routes(app):
    
    # Get all airports in Finland
    @app.route("/airports", methods=["GET"])
    def get_airports():
        try:
            airports = get_started_country()
            return jsonify({"airports": airports})
        except Exception as e:
            return {"error": str(e)}, 500
    
    # Get random airports from Finland (excluding HEL)
    @app.route("/random_airports", methods=["GET"])
    def get_random_airports():
        try:
            limit = request.args.get("limit", 3, type=int)
            airport = Airport("EFHK")  # Using Helsinki as base
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
            return jsonify(distance_data)
        except Exception as e:
            return {"error": str(e)}, 500
    
    # Save game state
    @app.route("/save_game", methods=["POST"])
    def save_game():
        data = request.json
        player_name = data.get("player_name") if data else None
        start_airport = data.get("start_airport") if data else None
        ending_airport = data.get("ending_airport") if data else None
        weather = data.get("weather") if data else None
        distance = data.get("distance", 0) if data else 0
        
        if not all([player_name, start_airport, ending_airport, weather]):
            return {"error": "player_name, start_airport, ending_airport, and weather are required"}, 400
        
        try:
            game = Game(player_name, start_airport, ending_airport, weather, distance)
            success = game.save_game_state()
            if success:
                return {"message": "Game saved successfully"}
            else:
                return {"error": "Failed to save game"}, 500
        except Exception as e:
            return {"error": str(e)}, 500
    
    # Get player status
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
    
    # Update player score based on difficulty
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
    

    @app.route('/ending_airport', methods= ["POST"])
    ## we gonna get here the ending airport from the user
    def ending_airport_choice():
        data = request.json
        ending_airport = data.get("ending_airport") if data else None
        if not ending_airport:
            return {"error": "Ending airport is required"}, 400
        return {"ending_airport": ending_airport} ## kys

## player post name,other nulls at the start 
    @app.route('/score', methods= ["POST"])
    def scores():
        data = request.json
        score = data.get("score") if data else None
        if not score:
            return {"error": "Score is required"}, 400
        return {"score": score}
    @app.route('/crashed', methods= ["POST"])
    def crashed():
        data = request.json
        crashed = data.get("crashed") if data else None
        if not crashed:
            return {"error": "Crashed status is required"}, 400
        return {"crashed": crashed} 
        
        
    return app