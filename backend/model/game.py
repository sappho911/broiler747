
from model.player import Player
import requests
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        database="flight_game",
        user="root",
        password="2004",
        autocommit=True
    )

class Game:
    def __init__(self, player_name, start_airport, ending_airport, weather, distance):
        self.player = Player(player_name, 0, 0, 0)
        self.start_airport = start_airport
        self.ending_airport = ending_airport
        self.weather = weather
        self.distancee = distance

        
    def distance(self,start_airport,ending_airport): ## note i know i shouldnt have done it like this but time  is ticking and fuck u also hiii chat
        api_key = "E2iJwihYC4fHgXMoxt6fvv1o "
        payload = {
            "start_airport": start_airport,
            "ending_airport": ending_airport
        }
        key =  requests.get(F"https://airportgap.com/api/airports/distance",headers = { "Authorization": f"Bearer {api_key}","Content-Type":  "application/json" }, params=payload) # Raise error for bad status codes
        
        data = key.json()
        return data
    
        
    def save_game_state(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            insert_sql = "INSERT INTO game (weather, player_name, start_airport, ending_airport, distancee ) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_sql, (self.weather, self.player.player_name, self.start_airport, self.ending_airport, self.distancee))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    