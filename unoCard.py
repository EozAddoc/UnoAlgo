import pygame
from settings import *
from uno import *

def draw_card(screen, card, x, y,  is_ai=False, rotate=False):
    card_width, card_height = SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.15
    color_map = {
        "R": (255, 0, 0),
        "G": (0, 255, 0),
        "B": (0, 0, 255),
        "Y": (255, 255, 0),
        "W": (128, 128, 128)
    }

    card_surface = pygame.Surface((card_width, card_height), pygame.SRCALPHA)

    if is_ai:
        pygame.draw.rect(card_surface, (100, 100, 100), (0, 0, card_width, card_height ), border_radius=10)
        pygame.draw.rect(card_surface, BLACK, (0, 0, card_width,card_height ), width=2, border_radius=10)
    else:
        card_color = color_map.get(card.color, BLACK)
        pygame.draw.rect(card_surface, card_color, (0, 0, card_width, card_height), border_radius=10)
        pygame.draw.rect(card_surface, BLACK, (0, 0, card_width, card_height), width=2, border_radius=10)

        font_size = int(SCREEN_HEIGHT * 0.05)
        font = pygame.font.Font(None, font_size)
        text = font.render(card.value, True, BLACK)
        text_rect = text.get_rect(center=(card_width // 2, card_height // 2))
        card_surface.blit(text, text_rect)
    if rotate:
        card_surface = pygame.transform.rotate(card_surface, 90)
   
    screen.blit(card_surface, (x, y))



def draw_hand(screen, player, start_x, start_y, is_ai=False, rotate=True):
    spacing = SCREEN_WIDTH * 0.12  
    if not rotate : 
        if is_ai:
            for i, card in enumerate(player.hand):
                draw_card(screen, card, start_x + i * SCREEN_WIDTH * 0.04, start_y, is_ai,rotate)
        else:
            for i, card in enumerate(player.hand):
                draw_card(screen, card, start_x + i * spacing, start_y, is_ai,rotate)
    else:
        for i, card in enumerate(player.hand):
            draw_card(screen, card, start_x, start_y + i *SCREEN_WIDTH * 0.04 ,  is_ai,rotate)

    

def display_hand(player, screen, position, is_ai=False, rotate=True):
    """Displays the player's hand (either cards or back of cards for AI players)."""
    draw_hand(screen, player, position[0], position[1], is_ai, rotate)
    
def display_other_players(players, screen):
    font = pygame.font.SysFont('Arial', 30)

    y_offset = 50
    for player in players:
        if isinstance(player, AIPlayer): 
            text = font.render(f"{player.name}: {len(player.hand)} cards", True, BLACK)
            screen.blit(text, (SCREEN_WIDTH - 200, y_offset))
        elif isinstance(player, Player):  
            text = font.render(f"{player.name}: {len(player.hand)} cards", True, BLACK)
            screen.blit(text, (SCREEN_WIDTH - 200, y_offset))
        y_offset += 40  

def display_discard_pile(discard_pile, screen):
    font = pygame.font.SysFont('Arial', 30)

    top_card_text = font.render(f"Discard Pile: {str(discard_pile.top_card)}", True, BLACK)
    screen.blit(top_card_text, (SCREEN_WIDTH // 2 - 150, 50))