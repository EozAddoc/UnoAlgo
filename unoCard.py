import pygame
from settings import *
from uno import *

def draw_card(screen, card, x, y):
    card_width, card_height = 80, 120
    color_map = {
        "R": (255, 0, 0),
        "G": (0, 255, 0),
        "B": (0, 0, 255),
        "Y": (255, 255, 0),
        "W": (128, 128, 128)
    }
    
    # Draw card rectangle
    card_color = color_map.get(card.color, BLACK)
    pygame.draw.rect(screen, card_color, (x, y, card_width, card_height), border_radius=10)
    pygame.draw.rect(screen, BLACK, (x, y, card_width, card_height), width=2, border_radius=10)
    font = pygame.font.Font(None, 36)  
    text = font.render(card.value, True, BLACK)
    text_rect = text.get_rect(center=(x + card_width // 2, y + card_height // 2))
    screen.blit(text, text_rect)

def draw_hand(screen, player, start_x, start_y, is_ai=False):
    """Draws the entire hand of cards for a player (real cards or back for AI)."""
    spacing = 100  # Space between cards
    for i, card in enumerate(player.hand):
        if isinstance(player, Player):  # Human Player: show real cards
            draw_card(screen, card, start_x + i * spacing, start_y)
        else:  # AI Player: display the back of the card (black rectangle)
            pygame.draw.rect(screen, BLACK, (start_x + i * spacing, start_y, 70, 100))  # Card back

def display_hand(player, screen, position, is_ai=False):
    """Displays the player's hand (either cards or back of cards for AI players)."""
    draw_hand(screen, player, position[0], position[1], is_ai)
def display_other_players(players, screen):
    font = pygame.font.SysFont('Arial', 30)

    # Display the number of cards each player has (without showing the cards)
    y_offset = 50
    for player in players:
        if isinstance(player, AIPlayer):  # AI player
            text = font.render(f"{player.name}: {len(player.hand)} cards", True, BLACK)
            screen.blit(text, (SCREEN_WIDTH - 200, y_offset))
        elif isinstance(player, Player):  # Human player
            text = font.render(f"{player.name}: {len(player.hand)} cards", True, BLACK)
            screen.blit(text, (SCREEN_WIDTH - 200, y_offset))
        y_offset += 40  # Move down for the next player

def display_discard_pile(discard_pile, screen):
    font = pygame.font.SysFont('Arial', 30)

    # Display the top card of the discard pile
    top_card_text = font.render(f"Discard Pile: {str(discard_pile.top_card)}", True, BLACK)
    screen.blit(top_card_text, (SCREEN_WIDTH // 2 - 150, 50))