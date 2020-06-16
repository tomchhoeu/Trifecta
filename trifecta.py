import pygame
import math
from pygame.locals import *
from enum import Enum

# Position: A spot represents one block of the 8×8 grid and an optional piece.
class Position:
    def __init__(self, x, y):
        self.piece = None
        self.x = x
        self.y = y
    def get_piece(self):
        return self.piece
    def set_piece(self, piece):
        self.piece = piece
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y 
    def remove_piece(self):
        self.piece = None

# Piece: The basic building block of the system, every piece will be placed on a spot. Piece class is an abstract class. 

class Piece:
    def __init__(self, kind, team):
        self.killed = False
        self.team = team
        self.kind = [kind]
        self.moves = 0
        self.reserve = []
    def is_white(self):
        return "white" == self.team
    def is_killed(self):
        return self.killed
    def kill_piece(self):
        self.killed = True
    def add_kind(self, kind):
        if self.is_add():
            if kind != "queen" and kind != "king":
                if len(self.kind) >= 3:
                    if self.is_only_pawn():
                        if kind == "pawn":
                            self.kind.append(kind)
                        else:
                            self.reserve += [kind]
                            print(self.reserve)
                    else:
                        self.reserve += [kind]
                        print(self.reserve)
                else:
                    self.kind.append(kind)
    def get_team(self):
        return self.team
    def get_kind(self):
        return self.kind
    def sort_kind(self):
        self.kind.sort()
        print(self.kind)
    def add_move(self):
        self.moves += 1
    def is_king(self):
        if ["king"] == self.kind:
            return True
        else:
            return False
    def is_queen(self):
        if ["queen"] == self.kind:
            return True
        else:
            return False
    def is_trifecta(self):
        if "rook" in self.kind and "bishop" in self.kind and "knight" in self.kind:
            return True
        else: 
            return False
    def is_triple_rook(self):
        if self.kind.count("rook") == 3:
            return True
        else: 
            return False
    def is_triple_bishop(self):
        if self.kind.count("bishop") == 3:
            return True
        else: 
            return False
    def is_triple_knight(self):
        if self.kind.count("knight") == 3:
            return True
        else: 
            return False
    def is_only_pawn(self):
        for kind in self.kind:
            if kind != "pawn":
                return False
        return True
    def is_empress(self):
        return self.is_only_pawn() and len(self.kind) == 5
    def select_move(self, x, y, squares, player):
        moves = []
        for kind in self.kind:
            if kind == "pawn":
                moves += (self.pawn_moves(x, y, squares, player))
            elif kind == "rook":
                moves += (self.rook_moves(x, y, squares, player))
            elif kind == "knight":
                moves += (self.knight_moves(x, y, squares, player))
            elif kind == "bishop":
                moves += (self.bishop_moves(x, y, squares, player))
            elif kind == "queen":
                moves += (self.bishop_moves(x, y, squares, player))
                moves += (self.rook_moves(x, y, squares, player))
            elif kind == "king":
                moves += (self.king_moves(x, y, squares, player)) #+ self.castle(x, y, squares, player)
        if self.is_triple_rook():
            moves += self.triple_rook_moves(x, y, squares, player)
        if self.is_empress():
            moves += (self.bishop_moves(x, y, squares, player))
            moves += (self.rook_moves(x, y, squares, player))
        return moves
    def rook_moves(self, x, y, squares, player):
        moves = []
        i = 1
        # up
        for i in range(1, 8):
            if x+i > 7:
                break
            if squares[x+i][y].get_piece() == None:
                # square is empty
                moves.append(squares[x+i][y])
            elif squares[x+i][y].get_piece().is_white() != player.is_white():
                # square has enemy
                moves.append(squares[x+i][y])
                break
            else:
                # square has ally
                break
        # down
        for i in range(1, 8):
            if x-i < 0:
                break
            if squares[x-i][y].get_piece() == None:
                # square is empty
                moves.append(squares[x-i][y])
            elif squares[x-i][y].get_piece().is_white() != player.is_white():
                # square has enemy
                moves.append(squares[x-i][y])
                break
            else:
                # square has ally
                break
        # left
        for i in range(1, 8):
            if y-i < 0:
                break
            if squares[x][y-i].get_piece() == None:
                # square is empty
                moves.append(squares[x][y-i])
            elif squares[x][y-i].get_piece().is_white() != player.is_white():
                # square has enemy
                moves.append(squares[x][y-i])
                break
            else:
                # square has ally
                break
        # right
        for i in range(1, 8):
            if y+i > 7:
                break
            if squares[x][y+i].get_piece() == None:
                # square is empty
                moves.append(squares[x][y+i])
            elif squares[x][y+i].get_piece().is_white() != player.is_white():
                # square has enemy
                moves.append(squares[x][y+i])
                break
            else:
                # square has ally
                break
        return moves 
    def knight_moves(self, x, y, squares, player):
        delta = [(1,2), (-1,2), (1,-2), (-1,-2), (2,1), (-2,1), (2,-1), (-2,-1)]
        moves = []
        for value in delta:
            if x + value[0] > 7 or y + value[1] > 7 or x + value[0] < 0 or y + value[1] < 0:
                continue
            square = squares[x+value[0]][y+value[1]]
            if square.get_piece() == None:
                  # square is empty
                moves.append(square)
            elif square.get_piece().is_white() != player.is_white():
                # square has enemy
                moves.append(square)
        return moves 
    def bishop_moves(self, x, y, squares, player):
        moves = []
        for i in range(1, 8):
            if y+i > 7 or x+i > 7:
                break
            square = squares[x+i][y+i]
            if square.get_piece() == None:
                # square is empty
                moves.append(square)
            elif square.get_piece().is_white() != player.is_white():
                # square has enemy
                moves.append(square)
                break
            else:
                # square has ally
                break
        for i in range(1, 8):
            if y-i < 0 or x+i > 7:
                break
            square = squares[x+i][y-i]
            if square.get_piece() == None:
                # square is empty
                moves.append(square)
            elif square.get_piece().is_white() != player.is_white():
                # square has enemy
                moves.append(square)
                break
            else:
                # square has ally
                break
        for i in range(1, 8):
            if y+i > 7 or x-i < 0:
                break
            square = squares[x-i][y+i]
            if square.get_piece() == None:
                # square is empty
                moves.append(square)
            elif square.get_piece().is_white() != player.is_white():
                # square has enemy
                moves.append(square)
                break
            else:
                # square has ally
                break
        for i in range(1, 8):
            if y-i < 0 or x-i < 0:
                break
            square = squares[x-i][y-i]
            if square.get_piece() == None:
                # square is empty
                moves.append(square)
            elif square.get_piece().is_white() != player.is_white():
                # square has enemy
                moves.append(square)
                break
            else:
                # square has ally
                break
        return moves 
    def king_moves(self, x, y, squares, player):
        delta = [(1,1), (-1,1), (1,-1), (-1,-1), (1,0), (0,1), (0,-1), (-1,0)]
        moves = []
        for value in delta:
            if x + value[0] > 7 or y + value[1] > 7 or x + value[0] < 0 or y + value[1] < 0:
                continue
            square = squares[value[0]+x][value[1]+y]
            if square.get_piece() == None:
                  # square is empty
                moves.append(square)
                print(square.get_x(), square.get_y())
                print("added!")
            elif square.get_piece().is_white() != player.is_white():
                # square has enemy
                moves.append(square)
        return moves 
    def pawn_moves(self, x, y, squares, player):
        direction = 0
        if player.is_white():
            direction = 1
        else:
            direction = -1
        moves = []
        # pawn attacks
        if y-1 >= 0 and x + direction >= 0 and x + direction <= 7:
            square = squares[x+direction][y-1]
            if square.get_piece() != None: 
                if square.get_piece().is_white() != player.is_white():
                    # square has enemy
                    moves.append(square)
        if y+1 <= 7 and x + direction >= 0 and x + direction <= 7:
            square = squares[x+direction][y+1]
            if square.get_piece() != None: 
                if square.get_piece().is_white() != player.is_white():
                    # square has enemy
                    moves.append(square)
        # pawn moving forward
        if x + direction >= 0 and x + direction <= 7:
            square = squares[x+direction][y]
            if square.get_piece() == None:
                moves.append(square)
                if x + direction*2 >= 0 and x + direction*2 <= 7:
                    square2 = squares[x+direction*2][y]
                    if square2.get_piece() == None and self.moves == 0:
                        moves.append(square2)
        return moves 
    def triple_rook_moves(self, x, y, squares, player):
        moves = []
        for i in range(0, 8):
            for j in range(0, 8):
                square = squares[i][j]
                if square.get_piece() == None:
                    moves.append(square)
        return moves
    def is_add(self):
        return not self.is_queen() and not self.is_king() and not self.is_trifecta() and not self.is_triple_bishop() and not self.is_triple_knight() and not self.is_triple_rook() and not self.is_empress()


# The extended classes (Pawn, King, Queen, Rook, Knight, Bishop) implements the abstracted operations.

# Board: Board is an 8×8 set of boxes containing all active chess pieces.

class Board:
    def __init__(self):
        self.set_board()
    def set_board(self):
        self.squares = [[Position(i, j) for i in range(8)] for j in range(8)]
        # Setting whtie pieces
        self.squares[0][0].set_piece(Piece("rook", "white"))
        self.squares[0][1].set_piece(Piece("knight", "white"))
        self.squares[0][2].set_piece(Piece("bishop", "white"))
        self.squares[0][3].set_piece(Piece("queen", "white"))
        self.squares[0][4].set_piece(Piece("king", "white"))
        self.squares[0][5].set_piece(Piece("bishop", "white"))
        self.squares[0][6].set_piece(Piece("knight", "white"))
        self.squares[0][7].set_piece(Piece("rook", "white"))
        for i in range(8):
            self.squares[1][i].set_piece(Piece("pawn", "white"))
        # Setting black pieces
        self.squares[7][0].set_piece(Piece("rook", "black"))
        self.squares[7][1].set_piece(Piece("knight", "black"))
        self.squares[7][2].set_piece(Piece("bishop", "black"))
        self.squares[7][3].set_piece(Piece("queen", "black"))
        self.squares[7][4].set_piece(Piece("king", "black"))
        self.squares[7][5].set_piece(Piece("bishop", "black"))
        self.squares[7][6].set_piece(Piece("knight", "black"))
        self.squares[7][7].set_piece(Piece("rook", "black"))
        for i in range(8):
            self.squares[6][i].set_piece(Piece("pawn", "black"))
    def get_square(self, x, y):
        return self.squares[x][y]
    def get_squares(self):
        return self.squares
    

# Player: Player class represents one of the participants playing the game.

class Player:
    def __init__(self, team):
        self.team = team
    def is_white(self):
        return self.team == "white"

# wow = Board()
# ayy = wow.squares[0][1].piece.knight_moves(0, 1, wow.squares, Player("white"))
# for position in ayy:
#     print(position.get_x(), position.get_y())

# Move: Represents a game move, containing the starting and ending spot. The Move class will also keep track of the player who made the move.

class Move:
    def __init__(self, player, start, end):
        self.player = player
        self.start = start
        self.end = end
        self.piece_moved = start.get_piece()
        self.piece_taken = end.get_piece()
    def get_start(self):
        return self.start
    def get_end(self):
        return self.end
    def get_piece_moved(self):
        return self.piece_moved
    def get_piece_taken(self):
        return self.piece_taken


# Game: This class controls the flow of a game. It keeps track of all the game moves, which player has the current turn, and the final result of the game.

class Status(Enum):
    ACTIVE = 0
    BLACK_WIN = 1
    WHITE_WIN = 2
    FORFEIT = 3
    STALEMATE = 4
    DRAW = 5

class Game:
    def __init__(self):
        self.setup()
    def setup(self):
        self.players = [Player("white"), Player("black")]
        self.board = Board()
        self.turn = self.players[0]
        self.moves_played = []
        self.game_state = Status.ACTIVE
    def get_board(self):
        return self.board
    def get_turn(self):
        return self.turn
    def is_end(self):
        return self.game_state != Status.ACTIVE
    def get_state(self):
        return self.game_state
    def set_state(self, state):
        self.game_state = state
    def playerMove(self, player, start_x, start_y, end_x, end_y):
        start = self.board.get_square(start_x, start_y)
        end = self.board.get_square(end_x, end_y)
        move = Move(player, start, end)
        return self.make_move(move, player)
    def make_move(self, move, player):
        piece = move.get_piece_moved()
        if piece == None:
            return False
        if player != self.turn:
            return False
        if piece.is_white() != player.is_white():
            return False
        # if piece.can_move() == False:
        #     return False
        destination = move.get_piece_taken()
        # TODO: implemetn trifecta bit
        if destination != None:
            destination.kill_piece()
            if piece.is_trifecta() and destination.is_trifecta():
                self.game_state = Status.DRAW
            for kind in destination.get_kind():
                piece.add_kind(kind)
                piece.sort_kind()
        # castle
        
        # store move
        self.moves_played.append(move)
        # move piece
        piece.add_move()
        move.get_end().set_piece(piece)
        move.get_start().remove_piece()
        # add is_king
        if destination != None and destination.is_king():
            if player.is_white(): 
                self.game_state = Status.WHITE_WIN
            else:
                self.game_state = Status.BLACK_WIN
  
        # set the current turn to the other player 
        if self.turn == self.players[0]:
            self.turn = self.players[1]
        else:
            self.turn = self.players[0]
        return True

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
    # on_init calls pygame.init() that initialize all PyGame modules. 
    # Then it create main display - 640x400 window and try to use hardware acceleration. 
    # At the end this routine sets _running to True.
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
        # print(event)
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
        # print(self.game.is_end())
        if self.game.is_end():
            print("woah")
    # _moves
        # returns a list of available moves for a specific piece
    # rook_moves
    # bishop_moves
    # knight_moves
    # pawn_moves
    # queen_moves
    # king_moves
    # valid_moves checks if move is valid.
    # get_moves for each type of piece in piece.type gets the moves and then removes the invalid moves. 
 
if __name__ == "__main__" :
    game = App()
    game.on_execute()