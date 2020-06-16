from game import Game
import pygame
import math
from pygame.locals import *

# App

WHITE, BLACK, RED = (255,255,255),(147,112,219),(255,69,0)
class App:
    def __init__(self):
        self._running = True
        self.game_display = None
        self.size = self.width, self.height = 800, 800
        self.square, self.n_squares, self.offset = 60, 8, 160
        self.game = Game()
        self.circles = []
        self.follow = None
        self.clicked = False
    def on_init(self):
        pygame.init()
        self.game_display = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.game_display.fill((255, 255, 255))
        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        location = pygame.mouse.get_pos()
        x, y = (math.floor((location[0]-160)/60), 7-math.floor((location[1]-160)/60))
        if x <= 7 and y <= 7 and x >= 0 and y >= 0:
            square = self.game.get_board().get_square(y, x)
            piece = square.get_piece()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if square in self.circles:
                    self.game.playerMove(self.game.turn, self.follow[0], self.follow[1], square.get_y(), square.get_x())
                    self.circles = []
                elif piece != None:
                    if piece.is_white() == self.game.turn.is_white():
                        self.clicked = True
                        self.follow = (y, x)
                        moves = piece.select_move(y, x, self.game.get_board().get_squares(), self.game.get_turn())
                        self.circles = moves

            if event.type == pygame.MOUSEBUTTONUP:
                if square in self.circles:
                    self.game.playerMove(self.game.turn, self.follow[0], self.follow[1], square.get_y(), square.get_x())
                    self.circles = []
                self.clicked = False
        else:
            if event.type == pygame.MOUSEBUTTONUP:
                self.clicked = False
    def on_loop(self):
        self.draw_board()
        self.draw_pieces()
        self.draw_piece()
        self.draw_circles(self.circles)
        self.game_end()
        pass
    def on_render(self):
        pygame.display.update()
        pass
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
    def draw_board(self):
        cnt = 0
        for i in range(self.n_squares):
            for z in range(self.n_squares):
                if cnt % 2 == 0:
                    pygame.draw.rect(self.game_display, WHITE,[self.offset + self.square * z, self.offset + self.square * i, self.square, self.square])
                else:
                    pygame.draw.rect(self.game_display, BLACK, [self.offset + self.square * z, self.offset + self.square * i, self.square, self.square])
                cnt +=1
            cnt -= 1
        # pygame.draw.rect(self.game_display, BLACK,[self.offset - self.square * 2, self.offset + self.square*1, self.square, self.square])
        # pygame.draw.rect(self.game_display, BLACK,[self.offset - self.square * 2, self.offset + self.square*6, self.square, self.square])

        pygame.draw.rect(self.game_display,BLACK,[self.offset, self.offset, self.n_squares * self.square - 1, self.n_squares * self.square-1],2)
    def draw_pieces(self):
        for x in range(8):
            for y in range (8):
                piece = self.game.get_board().get_square(x, y).get_piece()
                if piece != None:
                    path = 'assets\\'
                    path += piece.get_team() 
                    for kind in piece.get_kind():
                        path += kind
                    path += ".png"
                    image = pygame.image.load(str(path)) 
                    self.game_display.blit(image, (self.offset + y* self.square, self.offset + (7-x)* self.square)) 
    def draw_circles(self, locations):
        for location in locations:
            coordinate = (location.get_x()*self.square + 190, (7-location.get_y())*self.square + 190)
            pygame.draw.circle(self.game_display, RED, coordinate, 12)
    def draw_piece(self):
        if self.clicked:
            piece = self.game.get_board().get_square(self.follow[0], self.follow[1]).get_piece()
            if piece != None:
                path = 'assets\\'
                path += piece.get_team() 
                for kind in piece.get_kind():
                    path += kind
                path += ".png"
                image = pygame.image.load(str(path)) 
            
            self.game_display.blit(image, (pygame.mouse.get_pos()[0]-30, pygame.mouse.get_pos()[1]-30)) 
    def game_end(self):
        if self.game.is_end():
            print("woah")
 
if __name__ == "__main__" :
    game = App()
    game.on_execute()