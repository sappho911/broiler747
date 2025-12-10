
from model.player import Player
import requests
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        database="flight_game",
        user="root",
        password="tishchuk6370",
        autocommit=True
    )

class Game:
    def __init__(self, player_name, start_airport, ending_airport, weather, distance, difficulty=None):
        self.player = Player(player_name, 0, 0, 0)
        self.start_airport = start_airport
        self.ending_airport = ending_airport
        self.weather = weather
        self.distancee = distance
        self.difficulty = difficulty

        
    def distance(self,start_airport,ending_airport): 
        api_key = "E2iJwihYC4fHgXMoxt6fvv1o"
        payload = {
            "from": start_airport.upper(),
            "to": ending_airport.upper()
        }
        try:
            response = requests.post(
                "https://airportgap.com/api/airports/distance",
                headers={"Authorization": f"Bearer token={api_key}"},
                data=payload
            )
            response.raise_for_status()
            data = response.json()
            km = data.get("data", {}).get("attributes", {}).get("kilometers", 0)
            return {"km": round(km, 3)}
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "km": 0}
    
    
    def get_difficulty(self, distance_km):
        if distance_km < 250:
            return "easy"
        elif distance_km <= 500:
            return "medium"
        elif distance_km <= 1000:
            return "hard"
        else:
            return "hard"
    
    def save_game_state(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            check_player_sql = "SELECT Player_Name FROM player WHERE Player_Name = %s"
            cursor.execute(check_player_sql, (self.player.player_name,))
            result = cursor.fetchone()
            
            if not result:
                insert_player_sql = "INSERT INTO player (Player_Name, Easy_Score, Medium_Score, Hard_Score) VALUES (%s, %s, %s, %s)"
                cursor.execute(insert_player_sql, (self.player.player_name, 0, 0, 0))
            
           
            insert_sql = "INSERT INTO game (weather, player_name, start_airport, ending_airport, distancee, difficulty) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_sql, (self.weather, self.player.player_name, self.start_airport, self.ending_airport, self.distancee, self.difficulty))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    