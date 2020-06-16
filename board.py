from position import Position
from piece import Piece
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