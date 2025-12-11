
import random
from flask import jsonify, request

from api.SEED import quiz_questions
from model.airport import Airport, Select_weather, get_started_country, get_connection
from model.player import Player
from model.game import Game


def register_routes(app):

    @app.route("/airports", methods=["GET"])
    def fetch_airports():
        """Fetch list of starting airports."""
        try:
            countries = get_started_country()
            return jsonify({"airports": countries})
        except Exception as exc:
            return {"error": str(exc)}, 500

    @app.route("/random_airports", methods=["GET"])
    def random_airports():
        """Return a few random airports from Finland."""
        amount = request.args.get("limit", 3, type=int)
        try:
            temp_airport = Airport("EFHK")
            res = temp_airport.get_random_airports_from_finland(amount)
            return jsonify({"airports": res})
        except Exception as exc:
            return {"error": str(exc)}, 500

    @app.route("/distance", methods=["POST"])
    def distance_between():
        data = request.json or {}
        start = data.get("start_airport")
        target = data.get("ending_airport")

        if not start or not target:
            return {"error": "Both start_airport and ending_airport must be provided"}, 400

        try:
            # dummy game obj to reuse the distance method
            g = Game("tmp_user", start, target, "sunny", 0)
            d = g.distance(start, target)

            km = d.get("km", 0)
            diff = g.get_difficulty(km)
            return jsonify({"km": km, "difficulty": diff})
        except Exception as exc:
            return {"error": str(exc)}, 500


    @app.route("/save_game", methods=["POST"])
    def save_game_route():
        payload = request.json or {}

        required = ["player_name", "start_airport", "ending_airport", "weather"]
        if not all(k in payload and payload[k] for k in required):
            return {"error": "Missing one or more required fields"}, 400

        try:
            g = Game(
                payload["player_name"],
                payload["start_airport"],
                payload["ending_airport"],
                payload["weather"],
                0
            )

            d = g.distance(payload["start_airport"], payload["ending_airport"])
            km = d.get("km", 0)
            g.distancee = km
            g.difficulty = g.get_difficulty(km)

            if g.save_game_state():
                return {
                    "message": "Game saved",
                    "km": km,
                    "difficulty": g.difficulty
                }

            return {"error": "Unable to save game"}, 500

        except Exception as exc:
            return {"error": str(exc)}, 500


    @app.route("/player_status", methods=["POST"])
    def get_player_info():
        body = request.json or {}
        name = body.get("player_name")

        if not name:
            return {"error": "player_name is required"}, 400

        try:
            p = Player(
                name,
                body.get("easy_score", 0),
                body.get("medium_score", 0),
                body.get("hard_score", 0),
            )
            return jsonify(p.get_status())
        except Exception as exc:
            return {"error": str(exc)}, 500

    @app.route("/update_score", methods=["POST"])
    def upd_score():
        body = request.json or {}
        name = body.get("player_name")

        if not name:
            return {"error": "player_name missing"}, 400

        try:
            p = Player(name, 0, 0, 0)
            p.update_score(body.get("points", 0))

            if body.get("difficulty"):
                p.game_diff(body["difficulty"])

            return jsonify(p.get_status())
        except Exception as exc:
            return {"error": str(exc)}, 500


    @app.route("/weather", methods=["POST"])
    def choose_weather():
        body = request.json or {}
        weather = body.get("weather")
        nm = body.get("name")

        if not weather or not nm:
            return {"error": "Weather and name required"}, 400

        try:
            msg = Select_weather(weather)
            return {"message": msg, "name": nm}
        except Exception as exc:
            return {"error": str(exc)}, 500


    @app.route("/seed_quiz", methods=["GET"])
    def quiz_seed():
        return {"questions": quiz_questions(5)}

    @app.route("/refuel", methods=["POST"])
    def refuel_attempt():
        return {"refueled": random.choice([True, False])}

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
    def list_players():
        conn = get_connection()
        cr = conn.cursor()
        cr.execute("SELECT Player_Name FROM player")
        rows = cr.fetchall()
        out = [{"name": r[0]} for r in rows]
        cr.close()
        conn.close()
        return jsonify(out)

    @app.route("/api/players/stats", methods=["GET"])
    def fetch_stats():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT Player_Name, Easy_Score, Medium_Score, Hard_Score FROM player")
        items = [
            {"name": r[0], "easy_score": r[1], "medium_score": r[2], "hard_score": r[3]}
            for r in cur.fetchall()
        ]
        cur.close()
        conn.close()
        return jsonify(items)


    @app.route("/new_player", methods=["POST"])
    def new_player_route():
        data = request.json or {}
        nm = data.get("name")

        if not nm:
            return {"error": "Name required"}, 400

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO player (Player_Name, Easy_Score, Medium_Score, Hard_Score) VALUES (%s, 0, 0, 0)",
            (nm,),
        )
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
                "player_name": name,
                "difficulty": diff,
                "new_score": new_score,
                "previous_best": current,
                "updated": improved,
                "message": (
                    f"New high score: {new_score} on {diff}"
                    if improved else
                    f"Score {new_score} did not beat your best ({current})"
                )
            })

        except Exception as exc:
            return {"error": str(exc)}, 500

    return app
