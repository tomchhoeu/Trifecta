from enum import Enum

class Status(Enum):
    ACTIVE = 0
    BLACK_WIN = 1
    WHITE_WIN = 2
    FORFEIT = 3
    STALEMATE = 4
    DRAW = 5