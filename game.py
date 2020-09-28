from player import Player
from board import Board
from move import Move
from piece import *
from status import Status


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
        self.promote = None

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
    
    def get_promote(self):
        return self.promote

    def set_promote(self, kind):
        if kind == "queen":
            self.promote.set_piece(Queen(self.promote.get_piece().is_white()))
            self.promote = None
        elif kind == "rook":
            self.promote.set_piece(Rook(self.promote.get_piece().is_white()))
            self.promote = None
        elif kind == "bishop":
            self.promote.set_piece(Bishop(self.promote.get_piece().is_white()))
            self.promote = None
        elif kind == "knight":
            self.promote.set_piece(Knight(self.promote.get_piece().is_white()))
            self.promote = None


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
        delta_x = move.get_end().get_x() - move.get_start().get_x()

        # Castling 
        if piece.get_kind() == "king" and abs(delta_x) == 2:
            y = move.get_start().get_y()
            if delta_x < 0:
                start = self.board.get_square(y, 0)
                end = self.board.get_square(y, 3)
                end.set_piece(start.get_piece())
                start.remove_piece()
            else:
                start = self.board.get_square(y, 7)
                end = self.board.get_square(y, 5)
                end.set_piece(start.get_piece())
                start.remove_piece()
        
        delta_y = move.get_end().get_y() - move.get_start().get_y()
        end_piece = move.get_end().get_piece()
        #En Passant
        if piece.get_kind() == "pawn" and abs(delta_x) == abs(delta_y) and move.get_end().is_empty():
            end_piece = self.board.get_square(move.get_start().get_y(), move.get_end().get_x()).get_piece()
            self.board.get_square(move.get_start().get_y(), move.get_end().get_x()).remove_piece()

        # Trifecta
        if end_piece and (piece.get_kind() != "queen" and piece.get_kind() != "king"):
            if piece.is_compound():
                if end_piece.is_compound():
                    for p in end_piece.get_pieces():
                        piece.add_piece(p)
                else:
                    piece.add_piece(end_piece)
            else:
                temp = piece
                piece = Compound(temp.is_white())
                piece.add_piece(temp)
                if end_piece.is_compound():
                    for p in end_piece.get_pieces():
                        piece.add_piece(p)
                else:
                    piece.add_piece(end_piece)
        
        move.get_end().set_piece(piece)
        move.get_start().remove_piece()

        # TODO: promote
        if piece.get_kind() == "pawn" and (move.get_end().get_y() == 7 or move.get_end().get_y() == 0):
            self.promote = move.get_end()

        if piece.get_kind() == "bishop"*3:
            self.board.bishop3(move.get_end(), piece.is_white())
        
        if self.board.check_mate(not player.is_white()):
            if not self.board.check_check(not player.is_white()):
                self.game_state = Status.STALEMATE
                print("Draw")
            elif player.is_white():
                print("white won")
                self.game_state = Status.WHITE_WIN
            else:
                print("black won")
                self.game_state = Status.BLACK_WIN
        
        # store move
        self.moves_played.append(move)
        self.board.add_move(move)
        piece.add_move()
        if self.turn == self.players[0]:
            self.turn = self.players[1]
        else:
            self.turn = self.players[0]
        return True