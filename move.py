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