# Piece: The basic building block of the system, every piece will be placed on a start. Piece class is an abstract class. 
from abc import ABC, abstractmethod
from collections import Counter

class Piece(ABC):
    def __init__(self, is_white):
        self.team = is_white
        self.killed = False
        self.moves = 0
        super().__init__()
    
    def is_white(self):
        return self.team
    
    def set_white(self, is_white):
        self.team = is_white

    def is_killed(self):
        return self.killed

    def kill_piece(self):
        self.killed = True

    def can_move(self, board, start, end):
        if not start.is_empty():
            start_piece = start.get_piece()
            end_piece = None
            if not end.is_empty():
                end_piece = end.get_piece()
                if end_piece.get_kind() == "king":
                    return False
                if end_piece.get_kind() == "knight"*3:
                    return False
            end.set_piece(start_piece)
            start.remove_piece()
            if board.check_check(self.is_white()):
                start.set_piece(start_piece)
                end.set_piece(end_piece)
                return False
            start.set_piece(start_piece)
            end.set_piece(end_piece)
        return self.move(board, start, end)

    def add_move(self):
        self.moves += 1
    
    def get_moves(self):
        return self.moves

    def is_compound(self):
        return False

    @abstractmethod
    def get_kind(self):
        pass
    
    @abstractmethod
    def move(self, board, start, end):
        pass

class Compound(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.pieces = []
        self.allpieces = {}
        self.kinds = []
        self.set = False
        self.allpieces["pawn"] = 0
        self.allpieces["rook"] = 0
        self.allpieces["knight"] = 0
        self.allpieces["bishop"] = 0


    def move(self, board, start, end):
        for piece in self.pieces:
            if piece.move(board, start, end):
                return True
        return False
    
    def get_kind(self):
        self.kinds.sort()
        return "".join(self.kinds)

    def add_piece(self, piece):
        piece.set_white(self.is_white())
        if self.set == True:
            return
        if piece.get_kind() == "king" or piece.get_kind() == "queen":
            return
        if piece.get_kind() not in self.allpieces:
            return
        self.allpieces[piece.get_kind()] += 1
        # Check if allpieces has trifecta
        if self.allpieces["rook"] == 1 and self.allpieces["knight"] == 1 and self.allpieces["bishop"] == 1:
            self.set = True
            self.kinds = ["rook", "bishop", "knight"]
            self.pieces = [Rook(self.is_white()), Bishop(self.is_white()), Knight(self.is_white())]
            return
        if self.allpieces["rook"] == 3:
            self.kinds = ["rook"*3]
            self.pieces = [Rook(self.is_white()), Rook(self.is_white()), Rook(self.is_white()), Rook3(self.is_white())]
            self.set = True
            return
        if self.allpieces["knight"] == 3:
            self.kinds = ["knight"*3]
            self.pieces = [Knight(self.is_white()), Knight(self.is_white()), Knight(self.is_white())]
            self.set = True
            return
        if self.allpieces["bishop"] == 3:
            self.kinds = ["bishop"*3]
            self.pieces = [Bishop(self.is_white()), Bishop(self.is_white()), Bishop(self.is_white())]
            self.set = True
            return
        if self.allpieces["pawn"] == 5:
            self.kinds = ["pawn"*5]
            self.pieces = [Queen(self.is_white())]
            self.set = True
            return
        if self.kinds.count("pawn") == len(self.pieces) and len(self.pieces) < 5 and piece.get_kind() == "pawn":
            self.pieces.append(piece)
            self.kinds.append(piece.get_kind())
            return
        if piece.get_kind() != "pawn" and self.kinds.count("pawn") > 0 and len(self.pieces) == 3:
            for p in self.pieces:
                if p.get_kind() == "pawn":
                    self.pieces.remove(p)
                    self.kinds.remove("pawn")
                    break
            self.kinds.append(piece.get_kind())
            self.pieces.append(piece)
            return
        if len(self.kinds) >= 3:
            self.pieces.append(piece)
            return
        
        self.pieces.append(piece)
        self.kinds.append(piece.get_kind())
        
    
    def is_compound(self):
        return True
    
    def get_pieces(self):
        return self.pieces

    def remove_piece(self, name):
        pass

class Rook3(Piece):
    def move(self, board, start, end):
        if end.is_empty():
            return True
        return False

    def get_kind(self):
        return "rook"


class Rook(Piece):
    def move(self, board, start, end):
        if start.get_x() == end.get_x():
            if end.get_y() < start.get_y():
                for i in range(end.get_y()+1,  start.get_y()):
                    if not board.get_square(i, start.get_x()).is_empty():
                        return False
            else:
                for i in range(start.get_y()+1, end.get_y()):
                    if not board.get_square(i, start.get_x()).is_empty():
                        return False
            if end.is_empty() or end.get_piece().is_white() != self.is_white():
                return True
        if start.get_y() == end.get_y():
            if end.get_x() < start.get_x():
                for i in range(end.get_x()+1,  start.get_x()):
                    if not board.get_square(start.get_y(), i).is_empty():
                        return False
            else:
                for i in range(start.get_x()+1, end.get_x()):
                    if not board.get_square(start.get_y(), i).is_empty():
                        return False
            
            if end.is_empty() or end.get_piece().is_white() != self.is_white():
                return True
        return False

    def get_kind(self):
        return "rook"

class Knight(Piece):
    def move(self, board, start, end):
        delta_x = abs(start.get_x() - end.get_x())
        delta_y = abs(start.get_y() - end.get_y())
        if (delta_x == 2 and delta_y == 1) or (delta_x == 1 and delta_y == 2):
            if end.is_empty() or end.get_piece().is_white() != self.is_white():
                return True
        else:
            return False

    def get_kind(self):
        return "knight"

class Bishop(Piece):
    def move(self, board, start, end):
        delta_x = end.get_x() - start.get_x()
        delta_y = end.get_y() - start.get_y()
        sign_x = sign(delta_x)
        sign_y = sign(delta_y)
        if abs(delta_x) == abs(delta_y):
            for i in range(1, abs(delta_x)):
                if not board.get_square(start.get_y() + i*sign_y, start.get_x() + i*sign_x).is_empty():
                    return False
            if end.is_empty() or end.get_piece().is_white() != self.is_white():
                return True
        return False

    def get_kind(self):
        return "bishop"


class Queen(Piece):
    def move(self, board, start, end):
        b = Bishop(self.is_white())
        r = Rook(self.is_white())
        return b.move(board, start, end) or r.move(board, start, end)

    def get_kind(self):
        return "queen"

class Pawn(Piece):
    def move(self, board, start, end):
        direction = 1
        if not self.is_white():
            direction = -1
        if start.get_y() + direction == end.get_y():
            if start.get_x() == end.get_x():
                if not board.get_square(start.get_y() + direction, start.get_x()).is_empty():
                    return False
                return True
            if start.get_x() + 1 == end.get_x():
                if end.is_empty():
                    move = board.get_last_move()
                    if move != None:
                        if move.get_piece_moved().get_kind() == "pawn" and abs(move.get_start().get_y() - move.get_end().get_y()) == 2 and move.get_end().get_y() == start.get_y():
                            return True
                elif end.get_piece().is_white() != self.is_white():
                    return True
            if start.get_x() - 1 == end.get_x():
                if end.is_empty():
                    move = board.get_last_move()
                    if move != None:
                        if move.get_piece_moved().get_kind() == "pawn" and abs(move.get_start().get_y() - move.get_end().get_y()) == 2 and move.get_end().get_y() == start.get_y():
                            return True
                elif end.get_piece().is_white() != self.is_white():
                    return True
    
        if start.get_y() + direction*2 == end.get_y() and self.moves == 0 and start.get_x() == end.get_x():
            if not board.get_square(start.get_y() + direction, start.get_x()).is_empty():
                return False
            if not board.get_square(start.get_y() + direction*2, start.get_x()).is_empty():
                return False
            return True
        return False

    def get_kind(self):
        return "pawn"

class King(Piece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.in_check = False

    def move(self, board, start, end): 
        delta_x = abs(end.get_x() - start.get_x())
        delta_y = abs(end.get_y() - start.get_y())
        if delta_x**2 + delta_y**2 <= 2 and delta_x + delta_y > 0:
            if end.is_empty() or end.get_piece().is_white() != self.is_white():
                return True
        # king/rook moves = 0 empty space between king-rook
        if delta_x == 2 and delta_y == 0 and self.get_moves() == 0:
            return self.can_castle(board, start, end)
        return False

    def get_kind(self):
        return "king"

    def can_castle(self, board, start, end):
        if board.check_danger(self.is_white(), start):
            return False
        if end.get_x() == 2:
            rook = board.get_square(0, end.get_y()).get_piece()
            if rook != None and rook.get_kind() == "rook" and rook.get_moves() == 0:
                for i in range(1, 4):
                    if not board.get_square(end.get_y(), i).is_empty() or board.check_danger(self.is_white(), board.get_square(end.get_y(), i)):
                        return False
                return True
        elif end.get_x() == 6:
            rook = board.get_square(0, end.get_y()).get_piece()
            if rook != None and rook.get_kind() == "rook" and rook.get_moves() == 0:
                for i in range(5, 7):
                    if not board.get_square(end.get_y(), i).is_empty() or board.check_danger(self.is_white(), board.get_square(end.get_y(), i)):
                        return False
                return True
        return False

    def set_in_check(self, in_check):
        self.in_check = in_check

def sign(num):
    if num < 0:
        return -1
    else:
        return 1
        

# def rook_moves(self, x, y, squares, player):
#         moves = []
#         i = 1
#         # up
#         for i in range(1, 8):
#             if x+i > 7:
#                 break
#             if squares[x+i][y].get_piece() == None:
#                 # square is empty
#                 moves.append(squares[x+i][y])
#             elif squares[x+i][y].get_piece().is_white() != player.is_white():
#                 # square has enemy
#                 moves.append(squares[x+i][y])
#                 break
#             else:
#                 # square has ally
#                 break
#         # down
#         for i in range(1, 8):
#             if x-i < 0:
#                 break
#             if squares[x-i][y].get_piece() == None:
#                 # square is empty
#                 moves.append(squares[x-i][y])
#             elif squares[x-i][y].get_piece().is_white() != player.is_white():
#                 # square has enemy
#                 moves.append(squares[x-i][y])
#                 break
#             else:
#                 # square has ally
#                 break
#         # left
#         for i in range(1, 8):
#             if y-i < 0:
#                 break
#             if squares[x][y-i].get_piece() == None:
#                 # square is empty
#                 moves.append(squares[x][y-i])
#             elif squares[x][y-i].get_piece().is_white() != player.is_white():
#                 # square has enemy
#                 moves.append(squares[x][y-i])
#                 break
#             else:
#                 # square has ally
#                 break
#         # right
#         for i in range(1, 8):
#             if y+i > 7:
#                 break
#             if squares[x][y+i].get_piece() == None:
#                 # square is empty
#                 moves.append(squares[x][y+i])
#             elif squares[x][y+i].get_piece().is_white() != player.is_white():
#                 # square has enemy
#                 moves.append(squares[x][y+i])
#                 break
#             else:
#                 # square has ally
#                 break
#         return moves 

# class Piece:
#     def __init__(self, kind, team):
#         self.killed = False
#         self.team = team
#         self.kind = [kind]
#         self.moves = 0
#         self.reserve = []
#     def is_white(self):
#         return "white" == self.team
#     def is_killed(self):
#         return self.killed
#     def kill_piece(self):
#         self.killed = True
#     def add_kind(self, kind):
#         if self.is_add():
#             if kind != "queen" and kind != "king":
#                 if len(self.kind) >= 3:
#                     if self.is_only_pawn():
#                         if kind == "pawn":
#                             self.kind.append(kind)
#                         else:
#                             self.reserve += [kind]
#                     else:
#                         self.reserve += [kind]
#                 else:
#                     self.kind.append(kind)
#     def get_team(self):
#         return self.team
#     def get_kind(self):
#         return self.kind
#     def sort_kind(self):
#         self.kind.sort()
#     def add_move(self):
#         self.moves += 1
#     def is_king(self):
#         if ["king"] == self.kind:
#             return True
#         else:
#             return False
#     def is_queen(self):
#         if ["queen"] == self.kind:
#             return True
#         else:
#             return False
#     def is_trifecta(self):
#         if "rook" in self.kind and "bishop" in self.kind and "knight" in self.kind:
#             return True
#         else: 
#             return False
#     def is_triple_rook(self):
#         if self.kind.count("rook") == 3:
#             return True
#         else: 
#             return False
#     def is_triple_bishop(self):
#         if self.kind.count("bishop") == 3:
#             return True
#         else: 
#             return False
#     def is_triple_knight(self):
#         if self.kind.count("knight") == 3:
#             return True
#         else: 
#             return False
#     def is_only_pawn(self):
#         for kind in self.kind:
#             if kind != "pawn":
#                 return False
#         return True
#     def is_empress(self):
#         return self.is_only_pawn() and len(self.kind) == 5
#     def select_move(self, x, y, squares, player):
#         moves = []
#         for kind in self.kind:
#             if kind == "pawn":
#                 moves += (self.pawn_moves(x, y, squares, player))
#             elif kind == "rook":
#                 moves += (self.rook_moves(x, y, squares, player))
#             elif kind == "knight":
#                 moves += (self.knight_moves(x, y, squares, player))
#             elif kind == "bishop":
#                 moves += (self.bishop_moves(x, y, squares, player))
#             elif kind == "queen":
#                 moves += (self.bishop_moves(x, y, squares, player))
#                 moves += (self.rook_moves(x, y, squares, player))
#             elif kind == "king":
#                 moves += (self.king_moves(x, y, squares, player)) #+ self.castle(x, y, squares, player)
#         if self.is_triple_rook():
#             moves += self.triple_rook_moves(x, y, squares, player)
#         if self.is_empress():
#             moves += (self.bishop_moves(x, y, squares, player))
#             moves += (self.rook_moves(x, y, squares, player))
#         return moves
#     def rook_moves(self, x, y, squares, player):
#         moves = []
#         i = 1
#         # up
#         for i in range(1, 8):
#             if x+i > 7:
#                 break
#             if squares[x+i][y].get_piece() == None:
#                 # square is empty
#                 moves.append(squares[x+i][y])
#             elif squares[x+i][y].get_piece().is_white() != player.is_white():
#                 # square has enemy
#                 moves.append(squares[x+i][y])
#                 break
#             else:
#                 # square has ally
#                 break
#         # down
#         for i in range(1, 8):
#             if x-i < 0:
#                 break
#             if squares[x-i][y].get_piece() == None:
#                 # square is empty
#                 moves.append(squares[x-i][y])
#             elif squares[x-i][y].get_piece().is_white() != player.is_white():
#                 # square has enemy
#                 moves.append(squares[x-i][y])
#                 break
#             else:
#                 # square has ally
#                 break
#         # left
#         for i in range(1, 8):
#             if y-i < 0:
#                 break
#             if squares[x][y-i].get_piece() == None:
#                 # square is empty
#                 moves.append(squares[x][y-i])
#             elif squares[x][y-i].get_piece().is_white() != player.is_white():
#                 # square has enemy
#                 moves.append(squares[x][y-i])
#                 break
#             else:
#                 # square has ally
#                 break
#         # right
#         for i in range(1, 8):
#             if y+i > 7:
#                 break
#             if squares[x][y+i].get_piece() == None:
#                 # square is empty
#                 moves.append(squares[x][y+i])
#             elif squares[x][y+i].get_piece().is_white() != player.is_white():
#                 # square has enemy
#                 moves.append(squares[x][y+i])
#                 break
#             else:
#                 # square has ally
#                 break
#         return moves 
#     def knight_moves(self, x, y, squares, player):
#         delta = [(1,2), (-1,2), (1,-2), (-1,-2), (2,1), (-2,1), (2,-1), (-2,-1)]
#         moves = []
#         for value in delta:
#             if x + value[0] > 7 or y + value[1] > 7 or x + value[0] < 0 or y + value[1] < 0:
#                 continue
#             square = squares[x+value[0]][y+value[1]]
#             if square.get_piece() == None:
#                   # square is empty
#                 moves.append(square)
#             elif square.get_piece().is_white() != player.is_white():
#                 # square has enemy
#                 moves.append(square)
#         return moves 
#     def bishop_moves(self, x, y, squares, player):
#         moves = []
#         for i in range(1, 8):
#             if y+i > 7 or x+i > 7:
#                 break
#             square = squares[x+i][y+i]
#             if square.get_piece() == None:
#                 # square is empty
#                 moves.append(square)
#             elif square.get_piece().is_white() != player.is_white():
#                 # square has enemy
#                 moves.append(square)
#                 break
#             else:
#                 # square has ally
#                 break
#         for i in range(1, 8):
#             if y-i < 0 or x+i > 7:
#                 break
#             square = squares[x+i][y-i]
#             if square.get_piece() == None:
#                 # square is empty
#                 moves.append(square)
#             elif square.get_piece().is_white() != player.is_white():
#                 # square has enemy
#                 moves.append(square)
#                 break
#             else:
#                 # square has ally
#                 break
#         for i in range(1, 8):
#             if y+i > 7 or x-i < 0:
#                 break
#             square = squares[x-i][y+i]
#             if square.get_piece() == None:
#                 # square is empty
#                 moves.append(square)
#             elif square.get_piece().is_white() != player.is_white():
#                 # square has enemy
#                 moves.append(square)
#                 break
#             else:
#                 # square has ally
#                 break
#         for i in range(1, 8):
#             if y-i < 0 or x-i < 0:
#                 break
#             square = squares[x-i][y-i]
#             if square.get_piece() == None:
#                 # square is empty
#                 moves.append(square)
#             elif square.get_piece().is_white() != player.is_white():
#                 # square has enemy
#                 moves.append(square)
#                 break
#             else:
#                 # square has ally
#                 break
#         return moves 
#     def king_moves(self, x, y, squares, player):
#         delta = [(1,1), (-1,1), (1,-1), (-1,-1), (1,0), (0,1), (0,-1), (-1,0)]
#         moves = []
#         for value in delta:
#             if x + value[0] > 7 or y + value[1] > 7 or x + value[0] < 0 or y + value[1] < 0:
#                 continue
#             square = squares[value[0]+x][value[1]+y]
#             if square.get_piece() == None:
#                 # square is empty
#                 moves.append(square)
#             elif square.get_piece().is_white() != player.is_white():
#                 # square has enemy
#                 moves.append(square)
#         return moves 
#     def pawn_moves(self, x, y, squares, player):
#         direction = 0
#         if player.is_white():
#             direction = 1
#         else:
#             direction = -1
#         moves = []
#         # pawn attacks
#         if y-1 >= 0 and x + direction >= 0 and x + direction <= 7:
#             square = squares[x+direction][y-1]
#             if square.get_piece() != None: 
#                 if square.get_piece().is_white() != player.is_white():
#                     # square has enemy
#                     moves.append(square)
#         if y+1 <= 7 and x + direction >= 0 and x + direction <= 7:
#             square = squares[x+direction][y+1]
#             if square.get_piece() != None: 
#                 if square.get_piece().is_white() != player.is_white():
#                     # square has enemy
#                     moves.append(square)
#         # pawn moving forward
#         if x + direction >= 0 and x + direction <= 7:
#             square = squares[x+direction][y]
#             if square.get_piece() == None:
#                 moves.append(square)
#                 if x + direction*2 >= 0 and x + direction*2 <= 7:
#                     square2 = squares[x+direction*2][y]
#                     if square2.get_piece() == None and self.moves == 0:
#                         moves.append(square2)
#         return moves 
#     def triple_rook_moves(self, x, y, squares, player):
#         moves = []
#         for i in range(0, 8):
#             for j in range(0, 8):
#                 square = squares[i][j]
#                 if square.get_piece() == None:
#                     moves.append(square)
#         return moves
#     def is_add(self):
#         return not self.is_queen() and not self.is_king() and not self.is_trifecta() and not self.is_triple_bishop() and not self.is_triple_knight() and not self.is_triple_rook() and not self.is_empress()
