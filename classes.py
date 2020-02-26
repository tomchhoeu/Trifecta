from run import *
from pathlib import Path

class Piece:
    def __init__(self, kind, team, position):
        self.kind = kind
        self.team = team
        self.position = position
        self.moves = 0
    def draw(self):
        path = str(Path.home())
        path += "\\Trifecta\\assets\\" + self.team + self.kind + ".png"
        image = pygame.image.load(str(path)) 
        gameDisplay.blit(image, (160 + self.position[0]* SIZE, 160 + self.position[1]* SIZE)) 