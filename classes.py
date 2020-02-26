
from run import *

class Piece:
    def __init__(self, kind, team, position):
        self.kind = kind
        self.team = team
        self.position = position
        self.moves = 0
    def draw(self):
        path = r'C:\Users\Tom\Documents\Chess\assets'
        path += "\\" + self.team + self.kind + ".png"
        image = pygame.image.load(path) 
        gameDisplay.blit(image, (160 + self.position[0]* SIZE, 160 + self.position[1]* SIZE)) 