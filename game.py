from enum import Enum
from player import Player
from board import Board
from move import Move

class Status(Enum):
    ACTIVE = 0
    BLACK_WIN = 1
    WHITE_WIN = 2
    FORFEIT = 3
    STALEMATE = 4
    DRAW = 5

# Game: This class controls the flow of a game. It keeps track of all the game moves, which player has the current turn, and the final result of the game.

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