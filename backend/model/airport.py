from config.db_connection import get_connection

class Airport:
    def __init__(self, ident):
        self.ident = ident

        sql = "SELECT ident, name, latitude_deg, longitude_deg FROM Airport WHERE ident ='" +ident+"'"

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)

        if len(res) == 1:
            self.ident = res[0][0]
            self.name = res[0][1]
            self.latitude_deg = res[0][2]
            self.longitude_deg = res[0][3]
            # print(self.ident, self.name, self.latitude_deg, self.longitude_deg)

    def get_random_airports_from_finland(self, limits=3):
        sql = f" SELECT airport.name , airport.iata_code FROM airport INNER JOIN country ON airport.iso_country = country.iso_country WHERE country.name = 'Finland' AND airport.iata_code != '' AND airport.iata_code != 'HEL' ORDER BY RAND() LIMIT {limits}"
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
        airports = []
        for name, iata in res:
            airports.append({"name": name, "iata_code": iata})
        return airports
    


    # There is should be function witch is calculate a distance between airport using geopy we are using api for that 



    # function of calculation of consumption


    # function of fetching weather.

def Select_weather(Weather):
    conn = get_connection()
    cur = conn.cursor()
    insert_sql = "INSERT INTO player (weather) VALUES (%s)"
    cur.execute(insert_sql, (Weather,))
    conn.commit()
    cur.close()
    return f"Weather choice '{Weather}' saved successfully."

# a1 = Airport("EFHK")
# a1.get_random_airports_from_finland(5)



def get_started_country():  
    conn = get_connection()
    cur = conn.cursor()
    query = """
        SELECT airport.name, airport.iata_code, airport.latitude_deg, airport.longitude_deg
        FROM airport 
        INNER JOIN country ON airport.iso_country = country.iso_country 
        WHERE country.name = 'Finland' 
        AND airport.iata_code != '' 
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

def saver():
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
    