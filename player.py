# Player: Player class represents one of the participants playing the game.

class Player:
    def __init__(self, team):
        self.team = team
    def is_white(self):
        return self.team == "white"