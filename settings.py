# settings.py

# Screen settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (48, 160, 240)
# Fonts
import pygame
pygame.font.init()

FONT_MEDIUM = pygame.font.SysFont(None, 40)
FONT_SMALL = pygame.font.SysFont(None, 25)
FONT_LARGE = pygame.font.Font(None, 72)