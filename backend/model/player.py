## this is the player model for the game yihheeeed
class Player:
    def __init__(self, player_name, easy_score, medium_score, hard_score):
        self.player_name = player_name
        self.distance_traveled = 0
        self.easy_score = easy_score
        self.medium_score = medium_score
        self.hard_score = hard_score
        self.score = 0
    
    def update_score(self, points):
        self.score += points
        return self.score
    
    
    def game_diff(self, difficulty):
        if difficulty == "easy":
            self.easy_score = self.score / 6
        elif difficulty == "medium":
            self.medium_score = self.score / 4
        elif difficulty == "hard":
            self.hard_score = self.score / 2
        return self.score
    
    
 
  
    
    def get_status(self):
        return {
            "name": self.player_name,
            "easy_score": self.easy_score,
            "medium_score": self.medium_score,
            "hard_score": self.hard_score,
        }
  
    def __repr__(self):
        return f"Player(name={self.player_name}, score={self.score}, easy={self.easy_score}, medium={self.medium_score}, hard={self.hard_score})"
    
