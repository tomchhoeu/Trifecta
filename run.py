import pygame

SIZE = 60
WHITE, BLACK, RED = (255,255,255),(147,112,219),(255,69,0)
pygame.init()
gameDisplay = pygame.display.set_mode((800,800))
pygame.display.set_caption('Trifecta')
clock = pygame.time.Clock()

crashed = False