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
