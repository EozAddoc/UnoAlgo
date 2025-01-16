import pygame
from settings import *
from uno import *

def draw_card(screen, card, x, y,  is_ai=False, rotate=False,valid=False):
    card_width, card_height = SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.18
    color_map = {
        "R": (255, 0, 0),
        "G": (0, 255, 0),
        "B": (0, 0, 255),
        "Y": (209, 209, 50),
        "W": (128, 128, 128)
    }

    card_surface = pygame.Surface((card_width, card_height), pygame.SRCALPHA)

    if is_ai:
        pygame.draw.rect(card_surface, BLACK, (0, 0, card_width, card_height ), border_radius=10)
        pygame.draw.rect(card_surface, WHITE, (0, 0, card_width,card_height ), width=8, border_radius=10)
        oval_width, oval_height = card_width * 0.7, card_height * 0.8
        oval_x = (card_width - oval_width) // 2
        oval_y = (card_height - oval_height) // 2
        ellipse_surface = pygame.Surface((card_width, card_height), pygame.SRCALPHA)
        pygame.draw.ellipse(ellipse_surface, RED, (oval_x, oval_y, oval_width, oval_height))
        # Load and scale the logo image
        logo = pygame.image.load('logo.png')
        
        # Scale the PNG logo to fit inside the card (adjust size as needed)
        scaled_png = pygame.transform.scale(logo, (int(card_width * 0.55), int(card_height * 0.55)))  # 50% width, 20% height

        # Position the logo at the top center of the card
        png_rect = scaled_png.get_rect(center=(card_width // 2, card_height // 2))  # Top part of the card

        # Rotate the ellipse only
        rotated_ellipse = pygame.transform.rotate(ellipse_surface, -35)  # Rotate by -35 degrees
        rotated_rect = rotated_ellipse.get_rect(center=(card_width // 2, card_height // 2))

        card_surface.blit(rotated_ellipse, rotated_rect.topleft)

        card_surface.blit(scaled_png, png_rect.topleft)

    else:
        card_color = color_map.get(card.color, BLACK)
        pygame.draw.rect(card_surface, card_color, (0, 0, card_width, card_height), border_radius=10)
        pygame.draw.rect(card_surface, WHITE, (0, 0, card_width, card_height), width=8, border_radius=10)

        oval_width, oval_height = card_width * 0.7, card_height * 0.94
        oval_x = (card_width - oval_width) // 2
        oval_y = (card_height - oval_height) // 2
        ellipse_surface = pygame.Surface((card_width, card_height), pygame.SRCALPHA)
        pygame.draw.ellipse(ellipse_surface, WHITE, (oval_x, oval_y, oval_width, oval_height))


        rotated_ellipse = pygame.transform.rotate(ellipse_surface, -35)  
        rotated_rect = rotated_ellipse.get_rect(center=(card_width // 2, card_height // 2))
        card_surface.blit(rotated_ellipse, rotated_rect.topleft)

        font_size = int(SCREEN_HEIGHT * 0.05)
        large_font_size = int(SCREEN_HEIGHT * 0.08)
        font = pygame.font.Font(None, font_size)
        large_font = pygame.font.Font(None, large_font_size)

        text_top_left = font.render(card.value, True, WHITE)
        text_top_left_rect = text_top_left.get_rect(topleft=( 10,  10))  
        card_surface.blit(text_top_left, text_top_left_rect)

        shadow_offset = 2  

        shadow_text_center = large_font.render(card.value, True, BLACK) 
        shadow_rect_center = shadow_text_center.get_rect(center=(card_width // 2 + shadow_offset, card_height // 2 + shadow_offset))
        card_surface.blit(shadow_text_center, shadow_rect_center.topleft)

        text_center = large_font.render(card.value, True, card_color)  
        text_center_rect = text_center.get_rect(center=(card_width // 2, card_height // 2))
        card_surface.blit(text_center, text_center_rect.topleft)

        text_bottom_right = font.render(card.value, True, WHITE)
        text_bottom_right_rect = text_bottom_right.get_rect(bottomright=(card_width - 10, card_height - 10)) 
        card_surface.blit(text_bottom_right, text_bottom_right_rect)
        if valid :
            pygame.draw.rect(card_surface, RED, (0, 0, card_width, card_height), width=5, border_radius=10)
    if rotate:
        card_surface = pygame.transform.rotate(card_surface, 90)
   
    screen.blit(card_surface, (x, y))
    return card_surface.get_rect(topleft=(x, y))



def draw_hand(screen, player, start_x, start_y,discard_pile, is_ai=False, rotate=True):
    spacing = SCREEN_WIDTH * 0.12 
    spacingOthers =0.03
    valid_moves = player.valid_moves(discard_pile.top_card)
    card_rects = []
    max_cards = 7 
    hand_size = len(player.hand)
    if hand_size > 8:
        spacingOthers = 0.03
    if not rotate : 
        if is_ai:
            for i, card in enumerate(player.hand):
                draw_card(screen, card, start_x + i * SCREEN_WIDTH * spacingOthers, start_y, is_ai,rotate)
        else:
            for i, card in enumerate(player.hand):
                if card in valid_moves:
                    x=draw_card(screen, card, start_x + i * spacing, start_y, is_ai,rotate, valid=True)
                    card_rects.append(x)
                else:
                    x=draw_card(screen, card, start_x + i * spacing, start_y, is_ai,rotate, valid=False)
                    card_rects.append(x)
    else:
        for i, card in enumerate(player.hand):
            draw_card(screen, card, start_x, start_y + i *SCREEN_WIDTH * spacingOthers ,  is_ai,rotate,valid=False)
    return card_rects



    

def display_hand(player, screen, position,discard_pile, is_ai=False, rotate=True):
    return draw_hand(screen, player, position[0], position[1],discard_pile, is_ai, rotate)

def display_discard_pile(discard_pile, screen):
    font = pygame.font.SysFont('Arial', 30)

    top_card_text = font.render(f"Discard Pile: {str(discard_pile.top_card)}", True, BLACK)
    screen.blit(top_card_text, (SCREEN_WIDTH // 2 - 150, 50))