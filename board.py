from position import Position
from piece import *
# Board: Board is an 8×8 set of boxes containing all active chess pieces.

class Board:
    def __init__(self):
        self.set_board()
        self.moves_played = []

    def set_board(self):
        self.squares = [[Position(i, j) for i in range(8)] for j in range(8)]
        # Setting whtie pieces
        self.squares[0][0].set_piece(Rook(True))
        self.squares[0][1].set_piece(Knight(True))
        self.squares[0][2].set_piece(Bishop(True))
        self.squares[0][3].set_piece(Queen(True))
        self.squares[0][4].set_piece(King(True))
        self.squares[0][5].set_piece(Bishop(True))
        self.squares[0][6].set_piece(Knight(True))
        self.squares[0][7].set_piece(Rook(True))
        for i in range(8):
            self.squares[1][i].set_piece(Pawn(True))
        # # Setting black pieces
        self.squares[7][0].set_piece(Rook(False))
        self.squares[7][1].set_piece(Knight(False))
        self.squares[7][2].set_piece(Bishop(False))
        self.squares[7][3].set_piece(Queen(False))
        self.squares[7][4].set_piece(King(False))
        self.squares[7][5].set_piece(Bishop(False))
        self.squares[7][6].set_piece(Knight(False))
        self.squares[7][7].set_piece(Rook(False))
        for i in range(8):
            self.squares[6][i].set_piece(Pawn(False))
    
    def add_move(self, move):
        self.moves_played.append(move)

    def get_last_move(self):
        if len(self.moves_played) > 0:
            return self.moves_played[-1]
        return None

    def get_square(self, x, y):
        return self.squares[x][y]

    def get_squares(self):
        return self.squares

    def get_king(self, isWhite):
        for i in range(8):
            for j in range(8):
                if not self.squares[i][j].is_empty():
                    piece = self.squares[i][j].get_piece()
                    if piece.get_kind() == "king" and piece.is_white() == isWhite:
                        return self.squares[i][j]

    def check_check(self, is_white):
        king = self.get_king(is_white)
        for i in range(8):
            for j in range(8):
                if not self.squares[i][j].is_empty():
                    piece = self.squares[i][j].get_piece()
                    if piece.move(self, self.squares[i][j], king):
                        return True
        king.get_piece().set_in_check(False)
        return False

    def check_danger(self, is_white, position):
        for i in range(8):
            for j in range(8):
                if not self.squares[i][j].is_empty():
                    piece = self.squares[i][j].get_piece()
                    if piece.get_kind() == "king":
                        continue
                    if piece.is_white() != is_white and piece.move(self, self.squares[i][j], position):
                        return True
        return False
    
    def check_mate(self, isWhite):
        for i in range(8):
            for j in range(8):
                for k in range(8):
                    for l in range(8):
                        if not self.squares[i][j].is_empty():
                            piece = self.squares[i][j].get_piece()
                            if piece.is_white() == isWhite and piece.can_move(self, self.squares[i][j], self.squares[k][l]):
                                return False
        return True
    
    def bishop3(self, position, isWhite):
        x = position.get_x()
        y = position.get_y()
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for direction in directions:
            for i in range(1, 7):
                if x + i*direction[0] == 8 or y + i*direction[1] == 8:
                    break
                if x + i*direction[0] == -1 or y + i*direction[1] == -1:
                    break
                square = self.get_square(y + i*direction[1], x + i*direction[0])
                if not square.is_empty():
                    if square.get_piece().is_white() != isWhite and square.get_piece().get_kind() != "king":
                        square.remove_piece()
                    break
