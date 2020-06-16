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