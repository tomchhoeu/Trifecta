from functions import *
import time
from math import floor, sqrt
'''
Three classes
Chess - game itself
Board - rendering the board - maintaining rules
Pieces - moving and stuff
'''
# FONT
font = pygame.font.Font('freesansbold.ttf', 32) 
text = font.render('White Playing', True, BLACK, WHITE) 
text2 = font.render('Black Playing', True, BLACK, WHITE) 
textRect = text.get_rect() 
textRect2 = text2.get_rect() 
textRect.center = (400, 80)
textRect2.center = (400, 80) 

# FONT


class Board:
    def __init__(self, size, board_length, offset):
        self.size = size
        self.board_length = board_length
        self.offset = offset
        self.pieces = []
        self.__create_pieces()
        self.clicked = None
        self.moves = []
        self.takes = []
        self.danger_b = []
        self.danger_w = []
        self.turn = "white"
        self.checked = False


    def draw(self):
        cnt = 0
        for i in range(self.board_length):
            for z in range(self.board_length):
                if cnt % 2 == 0:
                    pygame.draw.rect(gameDisplay, WHITE,[self.offset + self.size * z, self.offset + self.size * i, self.size, self.size])
                else:
                    pygame.draw.rect(gameDisplay, BLACK, [self.offset + self.size * z, self.offset + self.size * i, self.size, self.size])
                cnt +=1
            cnt -= 1
        
        pygame.draw.rect(gameDisplay,BLACK,[self.offset, self.offset, self.board_length * self.size - 1, self.board_length * self.size-1],2)
        if self.clicked:
            clicked_x, clicked_y = self.clicked
            pygame.draw.rect(gameDisplay, RED,[self.offset + self.size * clicked_x, self.offset + self.size * clicked_y, self.size, self.size])
            if self.clicked[0] < 0 or self.clicked[1] < 0:
                self.danger_zone(self.turn) 
        
        self.in_danger((board.turn))
        #self.promotion()
        

    def __create_pieces(self):
        for i in range(8):
            self.pieces.append(Piece("pawn", "black", (i,1)))
            self.pieces.append(Piece("pawn", "white", (i,6)))

        self.pieces.append(Piece("rook", "black", (0,0)))
        self.pieces.append(Piece("rook", "black", (7,0)))
        self.pieces.append(Piece("knight", "black", (1,0)))
        self.pieces.append(Piece("knight", "black", (6,0)))
        self.pieces.append(Piece("bishop", "black", (2,0)))
        self.pieces.append(Piece("bishop", "black", (5,0)))
        self.pieces.append(Piece("queen", "black", (3,0)))
        self.pieces.append(Piece("king", "black", (4,0)))

        self.pieces.append(Piece("rook", "white", (0,7)))
        self.pieces.append(Piece("rook", "white", (7,7)))
        self.pieces.append(Piece("knight", "white", (1,7)))
        self.pieces.append(Piece("knight", "white", (6,7)))
        self.pieces.append(Piece("bishop", "white", (2,7)))
        self.pieces.append(Piece("bishop", "white", (5,7)))
        self.pieces.append(Piece("queen", "white", (3,7)))
        self.pieces.append(Piece("king", "white", (4,7)))


    def draw_pieces(self):
        for piece in self.pieces:
            piece.draw()
    

    def location(self, location):
        # Check if location set
        if self.clicked:
            clicked_x, clicked_y = self.clicked
            comparison = (floor((location[0]-160)/60), floor((location[1]-160)/60))
            
            if clicked_x == floor((location[0]-160)/60) and clicked_y == floor((location[1]-160)/60):
                self.clicked = None
                self.takes = []
                self.moves = []
            elif comparison in self.moves:
                self.move_piece(self.clicked, comparison)
                self.clicked = None
                self.takes = []
                self.moves = []
            elif comparison in self.takes:
                self.take_piece(self.clicked, comparison)
                self.clicked = None
                self.takes = []
                self.moves = []
        else:
            self.clicked = (floor((location[0]-160)/60), floor((location[1]-160)/60))
    

    def is_ally(self, team, position):
        for piece in self.pieces:
            if piece.position == position and piece.team == team:
                return True
        return False


    def get_piece(self, position):
        for piece in self.pieces:
            if piece.position == position:
                return piece
        return None

    # returns list of availiable moves
    def pick_moves(self, team, position):
        if self.checked == True:
            kind = self.get_piece(position).kind       
            if kind == "pawn":
                moves = self.pawn_moves(team, position)
            elif kind == "rook":
                moves = self.rook_moves(team, position)
            elif kind == "knight":
                moves = self.knight_moves(team, position)
            elif kind == "bishop":
                moves = self.bishop_moves(team, position)
            elif kind == "queen":
                moves = self.bishop_moves(team, position) + self.rook_moves(team, position)
            elif kind == "king":
                moves = self.king_moves(team, position) + self.castle(team, position)
                return moves
            # for move in moves:
            #     save = self.pieces
            #     move_piece(position, move)
            #     self.in_danger(team)
            #     if self.checked == True:
            #         moves.remove(move)
            #     self.pieces = save
        else: 
            kind = self.get_piece(position).kind       
            if kind == "pawn":
                return self.pawn_moves(team, position)
            elif kind == "rook":
                return self.rook_moves(team, position)
            elif kind == "knight":
                return self.knight_moves(team, position)
            elif kind == "bishop":
                return self.bishop_moves(team, position)
            elif kind == "queen":
                return self.bishop_moves(team, position) + self.rook_moves(team, position)
            elif kind == "king":
                return self.king_moves(team, position) + self.castle(team, position)
    
    
    def rook_moves(self, team, position):
        moves = []
        danger = []
        for i in range(1,8):
            if self.is_empty((position[0]+i, position[1])):
                moves.append((position[0]+i, position[1]))
            elif self.is_enemy(team, (position[0]+i, position[1])):
                self.takes.append((position[0]+i, position[1]))
                break
            else: 
                danger.append((position[0]+i, position[1]))
                break
        for i in range(1,8):
            if self.is_empty((position[0]-i, position[1])):
                moves.append((position[0]-i, position[1]))
            elif self.is_enemy(team, (position[0]-i, position[1])):
                self.takes.append((position[0]-i, position[1]))
                break
            else: 
                danger.append((position[0]-i, position[1]))
                break
        for i in range(1,8):
            if self.is_empty((position[0], position[1]+i)):
                moves.append((position[0], position[1]+i))
            elif self.is_enemy(team, (position[0], position[1]+i)):
                self.takes.append((position[0], position[1]+i))
                break
            else: 
                danger.append((position[0], position[1]+i))
                break
        for i in range(1,8):
            if self.is_empty((position[0], position[1]-i)):
                moves.append((position[0], position[1]-i))
            elif self.is_enemy(team, (position[0], position[1]-i)):
                self.takes.append((position[0], position[1]-i))
                break
            else: 
                danger.append((position[0], position[1]-i))
                break
        if team == "white":
            self.danger_w += danger
            self.danger_w += self.takes
        else:
            self.danger_b += danger
            self.danger_b += self.takes
        return moves
    
    
    def knight_moves(self, team, position):
        moves = []
        danger = []
        if self.is_empty((position[0]+2, position[1]+1)):
            moves.append((position[0]+2, position[1]+1))
        else: 
            danger.append((position[0]+2, position[1]+1))
        if self.is_empty((position[0]-2, position[1]+1)):
            moves.append((position[0]-2, position[1]+1))
        else: 
            danger.append((position[0]-2, position[1]+1))
        if self.is_empty((position[0]+2, position[1]-1)):
            moves.append((position[0]+2, position[1]-1))
        else: 
            danger.append((position[0]+2, position[1]-1))
        if self.is_empty((position[0]-2, position[1]-1)):
            moves.append((position[0]-2, position[1]-1))
        else: 
            danger.append((position[0]-2, position[1]-1))
        if self.is_empty((position[0]+1, position[1]+2)):
            moves.append((position[0]+1, position[1]+2))
        else: 
            danger.append((position[0]+1, position[1]+2))
        if self.is_empty((position[0]-1, position[1]+2)):
            moves.append((position[0]-1, position[1]+2))
        else: 
            danger.append((position[0]-1, position[1]+2))
        if self.is_empty((position[0]+1, position[1]-2)):
            moves.append((position[0]+1, position[1]-2))
        else: 
            danger.append((position[0]+1, position[1]-2))
        if self.is_empty((position[0]-1, position[1]-2)):
            moves.append((position[0]-1, position[1]-2))
        else: 
            danger.append((position[0]-1, position[1]-2))

        if self.is_enemy(team, (position[0]+2, position[1]+1)):
            self.takes.append((position[0]+2, position[1]+1))
        if self.is_enemy(team, (position[0]-2, position[1]+1)):
            self.takes.append((position[0]-2, position[1]+1))
        if self.is_enemy(team, (position[0]+2, position[1]-1)):
            self.takes.append((position[0]+2, position[1]-1))
        if self.is_enemy(team, (position[0]-2, position[1]-1)):
            self.takes.append((position[0]-2, position[1]-1))
        if self.is_enemy(team, (position[0]+1, position[1]+2)):
            self.takes.append((position[0]+1, position[1]+2))
        if self.is_enemy(team, (position[0]-1, position[1]+2)):
            self.takes.append((position[0]-1, position[1]+2))
        if self.is_enemy(team, (position[0]+1, position[1]-2)):
            self.takes.append((position[0]+1, position[1]-2))
        if self.is_enemy(team, (position[0]-1, position[1]-2)):
            self.takes.append((position[0]-1, position[1]-2))
        if team == "white":
            self.danger_w += danger
            self.danger_w += self.takes
        else:
            self.danger_b += danger
            self.danger_b += self.takes
        return moves
    
    
    def bishop_moves(self, team, position):
        moves = []
        danger = []
        for i in range(1,8):
            if self.is_empty((position[0]+i, position[1]+i)):
                moves.append((position[0]+i, position[1]+i))
            elif self.is_enemy(team, (position[0]+i, position[1]+i)):
                self.takes.append((position[0]+i, position[1]+i))
                break
            else: 
                danger.append((position[0]+i, position[1]+i))
                break
        for i in range(1,8):
            if self.is_empty((position[0]-i, position[1]-i)):
                moves.append((position[0]-i, position[1]-i))
            elif self.is_enemy(team, (position[0]-i, position[1]-i)):
                self.takes.append((position[0]-i, position[1]-i))
                break
            else: 
                danger.append((position[0]-i, position[1]-i))
                break
        for i in range(1,8):
            if self.is_empty((position[0]-i, position[1]+i)):
                moves.append((position[0]-i, position[1]+i))
            elif self.is_enemy(team, (position[0] - i, position[1]+i)):
                self.takes.append((position[0] - i, position[1]+i))
                break
            else: 
                danger.append((position[0] - i, position[1]+i))
                break
        for i in range(1,8):
            if self.is_empty((position[0]+i, position[1]-i)):
                moves.append((position[0]+i, position[1]-i))
            elif self.is_enemy(team, (position[0]+i, position[1]-i)):
                self.takes.append((position[0]+i, position[1]-i))
                break
            else: 
                self.danger.append((position[0]+i, position[1]-i))
                break
        if team == "white":
            self.danger_w += danger
            self.danger_w += self.takes
        else:
            self.danger_b += danger
            self.danger_b += self.takes
        return moves
    
    
    def king_moves(self, team, position):
        moves = []
        self.danger_zone(team)
        if self.is_empty((position[0], position[1] + 1)):
            moves.append((position[0], position[1] + 1))
        elif self.is_enemy(team, (position[0], position[1] + 1)):
            self.takes.append((position[0], position[1] + 1))
        if self.is_empty((position[0] + 1, position[1] - 1)):
            moves.append((position[0] + 1, position[1] - 1))
        elif self.is_enemy(team, (position[0] + 1, position[1] - 1)):
            self.takes.append((position[0] + 1, position[1] - 1))
        if self.is_empty((position[0] - 1, position[1] - 1)):
            moves.append((position[0] - 1, position[1] - 1))
        elif self.is_enemy(team, (position[0] - 1, position[1] - 1)):
            self.takes.append((position[0] - 1, position[1] - 1))
        if self.is_empty((position[0], position[1] - 1)):
            moves.append((position[0], position[1] - 1))
        elif self.is_enemy(team, (position[0], position[1] - 1)):
            self.takes.append((position[0], position[1] - 1))
        if self.is_empty((position[0] + 1, position[1])):
            moves.append((position[0] + 1, position[1]))
        elif self.is_enemy(team, (position[0] + 1, position[1])):
            self.takes.append((position[0] + 1, position[1]))
        if self.is_empty((position[0] - 1, position[1])):
            moves.append((position[0] - 1, position[1]))
        elif self.is_enemy(team, (position[0] - 1, position[1])):
            self.takes.append((position[0] - 1, position[1]))
        if self.is_empty((position[0] - 1, position[1] + 1)):
            moves.append((position[0] - 1, position[1] + 1))
        elif self.is_enemy(team, (position[0] - 1, position[1] + 1)):
            self.takes.append((position[0] - 1, position[1] + 1))
        if self.is_empty((position[0] + 1, position[1] + 1)):
            moves.append((position[0] + 1, position[1] + 1))
        elif self.is_enemy(team, (position[0] + 1, position[1] + 1)):
            self.takes.append((position[0] + 1, position[1] + 1))
        new_list0 = [x for x in self.takes if x not in self.danger]
        self.takes = new_list0
        new_list1 = [x for x in moves if x not in self.danger]
        
        return new_list1
    
    
    def pawn_moves(self, team, position):
        moves = []
        danger = []
        direc = 1
        if team == "white":
            direc = -1
        if self.is_empty((position[0], position[1] + direc)):
            if self.is_empty((position[0], position[1] + direc*2)) and self.n_moves(position) == 0:
                moves.append((position[0], position[1] + direc*2))
            moves.append((position[0], position[1] + direc))
        if self.is_enemy(team, (position[0]-1, position[1] + direc)):
            self.takes.append((position[0]-1, position[1] + direc))
        if self.is_enemy(team, (position[0]+1, position[1] + direc)):
            self.takes.append((position[0]+1, position[1] + direc))
        if team == "white":
            self.danger_w += danger
            self.danger_w += self.takes
        else:
            self.danger_b += danger
            self.danger_b += self.takes
        return moves
    
    
    def castle(self, tean, position):
        moves = []
        if self.n_moves(position) == 0:
            for i in range(1,3):
                if not self.is_empty((position[0]+i, position[1])):
                    break
            else:
                if self.n_moves((position[0]+3, position[1])) == 0:
                    moves.append((position[0] + 2, position[1]))
            for i in range(1,4):
                if not self.is_empty((position[0]-i, position[1])):
                    break
            else:
                if self.n_moves((position[0]-4, position[1])) == 0 :
                    moves.append((position[0] - 2, position[1]))
        return moves
    
    
    def pawn_attacks(self, team, position):
        moves = []
        danger = []
        direc = 1
        
        if team == "white":
            direc = -1
        if (position[0] - 1) >= 0 and (position[1] + direc) >= 0 and (position[1] + direc) <= 7:
            moves.append((position[0]-1, position[1] + direc))
        if (position[0] + 1) <= 7 and (position[1] + direc) >= 0 and (position[1] + direc) <= 7:
            moves.append((position[0]+1, position[1] + direc))
        if team == "white":
            self.danger_w += moves
        else:
            self.danger_b += moves
        return moves
        
    
    def is_empty(self, position):
        if position[0] >= 0 and position[0] < 8 and position[1] >= 0 and position[1] < 8:
            for piece in self.pieces:
                if piece.position == position:
                    return False
            return True
        return False
    
    
    def draw_circles(self, locations):
        self.moves = locations
        for location in locations:
            location = (location[0]*SIZE + 190, location[1]*SIZE + 190)
            pygame.draw.circle(gameDisplay, RED, location, 12)
    
    
    def move_piece(self, location1, location2):
        for piece in self.pieces:
            if piece.position == location1:
                if self.distance(location1, location2) == 2 and piece.kind == "king":
                    if location2[0] > 4:
                        self.move_piece((7,location1[1]),(5,location1[1]))
                    else:
                        self.move_piece((0,location1[1]),(3,location1[1]))
                    if self.turn == "white":
                        self.turn = "black"
                    else:
                        self.turn = "white"
                piece.position = location2
                piece.moves += 1
                if self.turn == "white":
                    self.turn = "black"
                else:
                    self.turn = "white"
        self.moves = []
        self.danger_zone(self.turn)
    def n_moves(self, position):
        for piece in self.pieces:
                if piece.position == position:
                    return piece.moves
    
    
    def get_team(self, position):
        for piece in self.pieces:
                    if piece.position == position:
                        return piece.team
   
   
    def take_piece(self, location1, location2):
        self.pieces.remove(self.get_piece(location2))
        # for piece in self.pieces:
        #     if piece.position == location2:
        #         self.pieces.remove(piece)
        #         break
        for piece in self.pieces:
            if piece.position == location1:
                piece.position = location2
                piece.moves += 1
                if self.turn == "white":
                    self.turn = "black"
                else:
                    self.turn = "white"
        # self.checked = False
        self.danger_zone(self.turn)
    
    def draw_takes(self):
        locations = self.takes
        for location in locations:
            #location = (location[0]*SIZE + 160, location[1]*SIZE + 160)
            
            pygame.draw.rect(gameDisplay,RED,[location[0]*SIZE + 160, location[1]*SIZE + 160, SIZE - 1, SIZE - 1], 2)

   
    def is_enemy(self, team, position):
        for piece in self.pieces:
            if piece.position == position and piece.team != team:
                return True
        return False
   
   
    def distance(self, position1, position2):
        return sqrt((position1[0] - position2[0])**2 + (position1[1] - position2[1])**2)
        
   
    def danger_zone(self, team):
        self.takes = []
        self.danger = []
        self.danger_w = []
        self.danger_b = []
        for piece in self.pieces:
            if piece.team != team:
                if piece.kind == "pawn":
                    self.takes += self.pawn_attacks(piece.team, piece.position)
                elif piece.kind == "king":
                    self.danger += [
                        (piece.position[0]+1, piece.position[1]+1),
                        (piece.position[0]+1, piece.position[1]-1),
                        (piece.position[0]+1, piece.position[1]),
                        (piece.position[0], piece.position[1]-1),
                        (piece.position[0]-1, piece.position[1]-1),
                        (piece.position[0]-1, piece.position[1]+1),
                        (piece.position[0]-1, piece.position[1]),
                        (piece.position[0], piece.position[1]),
                    ]
                else:
                    self.takes += self.pick_moves(piece.team, piece.position)
        self.danger += self.takes
        # Removes duplicates
        self.danger = list(dict.fromkeys(self.danger))
        self.in_board()
        self.draw_danger(team)
        self.takes = []
        self.moves = []
        
   
    def draw_danger(self, team):
        if team == "white":
            
            locations = self.danger_b
        else:
            locations = self.danger_w
        # locations = self.danger
        for location in locations:
            pygame.draw.rect(gameDisplay,RED,[location[0]*SIZE + 160, location[1]*SIZE + 160, SIZE, SIZE])
   
    # TODO: Add DANGER_W/_B
    def in_board(self):
        for i in range(100):
            for position in self.danger:
                if position[0] > 7 or position[0] < 0 or position[1] > 7 or position[1] < 0:
                    #self.danger.remove(position)
                    break


    def in_danger(self, team):
        if team == "white":
            danger = self.danger_b
        else:
            danger = self.danger_w
        for piece in self.pieces:
            if piece.kind == "king" and piece.team == team:
                if piece.position in danger:
                    self.draw_check(piece.position)
                    self.checked = True
    

    def other_team(self, team):
        if team == "white":
            return "black"
        else:
            return "white"


    def draw_check(self, position):
        path = str(Path.home())
        path += "\\Trifecta\\assets\\" + "check.png"
        image = pygame.image.load(path)
        gameDisplay.blit(image, (160 + position[0]* SIZE, 160 + position[1]* SIZE))


board = Board(60, 8, 160)
is_mouse_down = False

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
    
        #print(event)
    gameDisplay.fill((255, 255, 255))
    board.draw()
    
    if board.turn == "white":
        gameDisplay.blit(text, textRect) 
    else:
        gameDisplay.blit(text2, textRect2) 
        
    if pygame.mouse.get_pressed()[0] and not is_mouse_down:
        board.location(pygame.mouse.get_pos())
        is_mouse_down = True
    elif not pygame.mouse.get_pressed()[0] and is_mouse_down:
        is_mouse_down = False
    
    if board.is_ally(board.turn, board.clicked):
        board.draw_circles(board.pick_moves(board.turn, board.clicked))
        board.draw_takes()

    board.draw_pieces()
    
    
    pygame.display.update()
    clock.tick(1000)
