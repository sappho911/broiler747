import string, random
import config
from backend.config.db_connection import get_connection
from airport import Airport


class Game:
    def __init__(self, id, location, consumption, player=None):

        # this is like our stateGame from previous project
        # object where all our states of player.
        self.status = {}

        # this is where we add location where player was or visited it.
        # better ofcourse rewrite our DB table 'Game' and add some new stuff like
        #  score.
        self.location = []

        if id == 0:

            # there is we generate our path.
            random_path = string.ascii_lowercase + string.ascii_uppercase + string.digits

            self.status = {
                'id' : ''.join(random.choice(random_path) for i in range(15)),
                'name' : player,
                'co2': {
                    'consumed': config.co2_initial,
                    'budget': config.co2_budget,
                }
            }
            self.location.append(Airport(location))

            sql = "INSERT INTO Game VALUES ('" + self.status["id"] + "', " + str(self.status["co2"]["consumed"])
            sql += ", " + str(self.status["co2"]["budget"]) + ", '" + location + "', '" + self.status["name"] + "')"
            # print(sql)
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(sql)






            #update game functions.









#             connection.commit()
#
#             sql333 = "SELECT * FROM Game WHERE id = %s"
#             cursor.execute(sql333, (self.status["id"],))
#             res = cursor.fetchone()
#
#             print("status", res)
#
#     def __repr__(self):
#         return f"Game(status={self.status}, location={self.location} )"
#
# g1 = Game(0,'EFHK',0,'Alex')
# print(g1)

