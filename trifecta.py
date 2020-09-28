from game import Game
from status import Status
import pygame
import math
from pygame.locals import *
from pygame.gfxdraw import *
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
        if self.game.get_promote() != None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if location[0] >= 60 and location[0] <= 120:
                    if location[1] >= 220 and location[1] <= 280:
                        self.game.set_promote("queen")
                    if location[1] >= 280 and location[1] <= 340:
                        self.game.set_promote("rook")
                    if location[1] >= 340 and location[1] <= 400:
                        self.game.set_promote("bishop")
                    if location[1] >= 400 and location[1] <= 460:
                        self.game.set_promote("knight")
        elif x <= 7 and y <= 7 and x >= 0 and y >= 0:
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
                        board = self.game.get_board()
                        moves = []
                        for i in range(8):
                            for j in range(8):
                                if piece.can_move(board, board.get_square(y, x), board.get_square(i, j)):
                                    moves.append(board.get_square(i, j))
                        self.circles = moves

            if event.type == pygame.MOUSEBUTTONUP:
                if square in self.circles:
                    self.game.playerMove(self.game.turn, self.follow[0], self.follow[1], square.get_y(), square.get_x())
                    self.circles = []
                    self.follow = None
                self.clicked = False
        else:
            if event.type == pygame.MOUSEBUTTONUP:
                self.clicked = False

    def on_loop(self):
        self.game_end()
        pass

    def on_render(self):
        self.game_display.fill((255, 255, 255))
        self.draw_board()
        self.draw_check()
        self.draw_clicked()
        self.draw_pieces()
        self.draw_piece()
        self.draw_circles(self.circles)
        self.draw_promote()
        pygame.display.update()
        pass

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        while(self._running):
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
        pygame.draw.rect(self.game_display,BLACK,[self.offset, self.offset, self.n_squares * self.square - 1, self.n_squares * self.square-1],2)

    def draw_pieces(self):
        for x in range(8):
            for y in range (8):
                piece = self.game.get_board().get_square(x, y).get_piece()
                if piece != None:
                    path = 'assets\\'
                    if piece.is_white():
                        path += "white"
                    else:
                        path += "black"
                    for kind in piece.get_kind():
                        path += kind
                    path += ".png"
                    image = pygame.image.load(str(path)) 
                    self.game_display.blit(image, (self.offset + y* self.square, self.offset + (7-x)* self.square)) 

    def draw_circles(self, locations):
        for location in locations:
            x, y = location.get_x()*self.square + 190, (7-location.get_y())*self.square + 190
            # pygame.draw.circle(self.game_display, RED, coordinate, 12)
            pygame.gfxdraw.aacircle(self.game_display, x, y, 10, RED)
            pygame.gfxdraw.filled_circle(self.game_display, x, y, 10, RED)

    def draw_piece(self):
        if self.clicked:
            piece = self.game.get_board().get_square(self.follow[0], self.follow[1]).get_piece()
            if piece != None:
                path = 'assets\\'
                if piece.is_white():
                    path += "white"
                else:
                    path += "black"
                for kind in piece.get_kind():
                    path += kind
                path += ".png"
                image = pygame.image.load(str(path))
            
            self.game_display.blit(image, (pygame.mouse.get_pos()[0]-30, pygame.mouse.get_pos()[1]-30)) 

    def draw_check(self):
        position = None
        if self.game.get_turn().is_white():
            if self.game.get_board().check_check(True):
                position = self.game.get_board().get_king(True)
        else:
            if self.game.get_board().check_check(False):
                position = self.game.get_board().get_king(False)
        if position == None:
            return
        image = pygame.image.load("assets/check.png")
        self.game_display.blit(image, (position.get_x()*self.square + 160, (7 - position.get_y())*self.square + 160)) 
        pass

    def draw_clicked(self):
        if self.follow:
            image = pygame.image.load("assets/clicked.png")
            self.game_display.blit(image, (self.follow[1]*self.square + 160, (7 - self.follow[0])*self.square + 160)) 

    def draw_promote(self):
        if self.game.get_promote() != None:
            team = ""
            if self.game.get_promote().get_piece().is_white():
                team = "white"
            else:
                team = "black"
            image1 = pygame.image.load("assets/" + team + "queen.png")
            self.game_display.blit(image1, (60, 220)) 
            image2 = pygame.image.load("assets/" + team + "rook.png")
            self.game_display.blit(image2, (60, 280)) 
            image3 = pygame.image.load("assets/" + team + "bishop.png")
            self.game_display.blit(image3, (60, 340)) 
            image4 = pygame.image.load("assets/" + team + "knight.png")
            self.game_display.blit(image4, (60, 400)) 

    def game_end(self):
        if self.game.is_end():
            font = pygame.font.SysFont(None, 30)
            img = None
            
            if self.game.get_state() == Status.WHITE_WIN:
                
                img = font.render('White Wins!', True, BLACK)
                
            elif self.game.get_state() == Status.BLACK_WIN: 
                img = font.render('Black Wins!', True, BLACK)
            else:
                img = font.render('Draw!', True, BLACK)
            text_rect = img.get_rect(center=(self.width/2, 50))
            self.game_display.blit(img, text_rect)

if __name__ == "__main__" :
    game = App()
    game.on_execute()