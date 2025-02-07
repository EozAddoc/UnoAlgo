import pygame 
from settings import * 
from uno import * 

def draw_card(screen, card, x, y,  is_ai=False, rotate=False,valid=False): #56
    """
    Draws a UNO card on the screen at the specified position.

    Parameters:
    - screen (pygame.Surface): The game window where the card is drawn.
    - card (UnoCard): The card to be drawn.
    - x (int): The x-coordinate of the card's top-left position.
    - y (int): The y-coordinate of the card's top-left position.
    - is_ai (bool, optional): If True, draws a face-down card for AI players. Defaults to False.
    - rotate (bool, optional): If True, rotates the card 90 degrees. Defaults to False.
    - valid (bool, optional): If True, highlights the card with a red border if it's a valid move. Defaults to False.

    Returns:
    - pygame.Rect: The rectangle representing the drawn card's position.
    """
    card_width, card_height = SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.18 #1
    color_map = { #5
        "R": (255, 0, 0), #1
        "G": (0, 255, 0), #1
        "B": (0, 0, 255), #1
        "Y": (209, 209, 50), #1
        "W": (128, 128, 128) #1
    } 
 
    card_surface = pygame.Surface((card_width, card_height), pygame.SRCALPHA) #1

    if is_ai: #1
        pygame.draw.rect(card_surface, BLACK, (0, 0, card_width, card_height ), border_radius=10) #1
        pygame.draw.rect(card_surface, WHITE, (0, 0, card_width,card_height ), width=8, border_radius=10) #1
        oval_width, oval_height = card_width * 0.7, card_height * 0.8 #1
        oval_x = (card_width - oval_width) // 2 #1
        oval_y = (card_height - oval_height) // 2 #1
        ellipse_surface = pygame.Surface((card_width, card_height), pygame.SRCALPHA) #1
        pygame.draw.ellipse(ellipse_surface, RED, (oval_x, oval_y, oval_width, oval_height)) #1
        # Load and scale the logo image
        logo = pygame.image.load('logo.png') #1
    
        # Scale the PNG logo to fit inside the card (adjust size as needed) 
        scaled_png = pygame.transform.scale(logo, (int(card_width * 0.55), int(card_height * 0.55)))  # 50% width, 20% height #1
 
        # Position the logo at the top center of the card 
        png_rect = scaled_png.get_rect(center=(card_width // 2, card_height // 2))  # Top part of the card #1
 
        # Rotate the ellipse only 
        rotated_ellipse = pygame.transform.rotate(ellipse_surface, -35)  # Rotate by -35 degrees #1
        rotated_rect = rotated_ellipse.get_rect(center=(card_width // 2, card_height // 2)) #1
 
        card_surface.blit(rotated_ellipse, rotated_rect.topleft) #1
 
        card_surface.blit(scaled_png, png_rect.topleft) #1
 
    else: 
        card_color = color_map.get(card.color, BLACK) #1
        pygame.draw.rect(card_surface, card_color, (0, 0, card_width, card_height), border_radius=10) #1
        pygame.draw.rect(card_surface, WHITE, (0, 0, card_width, card_height), width=8, border_radius=10) #1
 
        oval_width, oval_height = card_width * 0.7, card_height * 0.94 #1
        oval_x = (card_width - oval_width) // 2 #1
        oval_y = (card_height - oval_height) // 2 #1
        ellipse_surface = pygame.Surface((card_width, card_height), pygame.SRCALPHA) #1
        pygame.draw.ellipse(ellipse_surface, WHITE, (oval_x, oval_y, oval_width, oval_height)) #1

        rotated_ellipse = pygame.transform.rotate(ellipse_surface, -35)   #1
        rotated_rect = rotated_ellipse.get_rect(center=(card_width // 2, card_height // 2)) #1
        card_surface.blit(rotated_ellipse, rotated_rect.topleft) #1
 
        font_size = int(SCREEN_HEIGHT * 0.05) #1
        large_font_size = int(SCREEN_HEIGHT * 0.08) #1
        font = pygame.font.Font(None, font_size) #1
        large_font = pygame.font.Font(None, large_font_size) #1
 
        text_top_left = font.render(card.value, True, WHITE) #1
        text_top_left_rect = text_top_left.get_rect(topleft=( 10,  10))   #1
        card_surface.blit(text_top_left, text_top_left_rect) #1
 
        shadow_offset = 2   #1
 
        shadow_text_center = large_font.render(card.value, True, BLACK)  #1
        shadow_rect_center = shadow_text_center.get_rect(center=(card_width // 2 + shadow_offset, card_height // 2 + shadow_offset)) #1
        card_surface.blit(shadow_text_center, shadow_rect_center.topleft) #1
 
        text_center = large_font.render(card.value, True, card_color)   #1
        text_center_rect = text_center.get_rect(center=(card_width // 2, card_height // 2)) #1
        card_surface.blit(text_center, text_center_rect.topleft) #1

        text_bottom_right = font.render(card.value, True, WHITE) #1
        text_bottom_right_rect = text_bottom_right.get_rect(bottomright=(card_width - 10, card_height - 10))  #1
        card_surface.blit(text_bottom_right, text_bottom_right_rect) #1
        if valid : #1
            pygame.draw.rect(card_surface, RED, (0, 0, card_width, card_height), width=5, border_radius=10) #1
    if rotate: #1
        card_surface = pygame.transform.rotate(card_surface, 90) #1
    
    screen.blit(card_surface, (x, y)) #1
    return card_surface.get_rect(topleft=(x, y)) #1

def draw_hand(screen, player, start_x, start_y,discard_pile, is_ai=False, rotate=True): #9 +8n
    """
    Draws the player's hand of UNO cards on the screen.

    Parameters:
    - screen (pygame.Surface): The game window where the hand is displayed.
    - player (UnoPlayer): The player whose hand is being drawn.
    - start_x (int): The starting x-coordinate for drawing the hand.
    - start_y (int): The starting y-coordinate for drawing the hand.
    - discard_pile (UnoPile): The discard pile to determine valid moves.
    - is_ai (bool, optional): If True, renders face-down cards for AI players. Defaults to False.
    - rotate (bool, optional): If True, rotates cards vertically for specific positions. Defaults to True.

    Returns:
    - list[pygame.Rect]: A list of rectangles representing each card's position.
    """
    spacing = SCREEN_WIDTH * 0.12  #1
    spacingOthers =0.03 #1
    valid_moves = player.valid_moves(discard_pile.top_card) # n+1
    card_rects = [] #1
    hand_size = len(player.hand) #1
    if hand_size > 8: #1
        spacingOthers = 0.03 #1
    if not rotate :  #1
        if is_ai: #1
            for i, card in enumerate(player.hand): #n
                draw_card(screen, card, start_x + i * SCREEN_WIDTH * spacingOthers, start_y, is_ai,rotate) #1
        else: 
            for i, card in enumerate(player.hand): #5n
                if card in valid_moves: #1
                    x=draw_card(screen, card, start_x + i * spacing, start_y, is_ai,rotate, valid=True) #1
                    card_rects.append(x) #1
                else: 
                    x=draw_card(screen, card, start_x + i * spacing, start_y, is_ai,rotate, valid=False) #1
                    card_rects.append(x) #1
    else: 
        for i, card in enumerate(player.hand): #n
            draw_card(screen, card, start_x, start_y + i *SCREEN_WIDTH * spacingOthers ,  is_ai,rotate,valid=False) #1
    return card_rects #1

def display_hand(player, screen, position,discard_pile, is_ai=False, rotate=True): #10 +8n
    """
    Displays the player's hand on the screen at the given position.

    Parameters:
    - player (UnoPlayer): The player whose hand is displayed.
    - screen (pygame.Surface): The game window.
    - position (tuple[int, int]): The (x, y) coordinates where the hand should be drawn.
    - discard_pile (UnoPile): The discard pile to check for valid moves.
    - is_ai (bool, optional): If True, displays AI cards face-down. Defaults to False.
    - rotate (bool, optional): If True, rotates cards vertically. Defaults to True.

    Returns:
    - list[pygame.Rect]: A list of rectangles representing the drawn cards.
    """
    return draw_hand(screen, player, position[0], position[1],discard_pile, is_ai, rotate) #1
 
def display_discard_pile(discard_pile, screen): #3
    """
    Displays the discard pile's top card on the screen.

    Parameters:
    - discard_pile (UnoPile): The discard pile whose top card is displayed.
    - screen (pygame.Surface): The game window where the discard pile is shown.

    Returns:
    - None
    """
    font = pygame.font.SysFont('Arial', 30) #1
    top_card_text = font.render(f"Discard Pile: {str(discard_pile.top_card)}", True, BLACK) #1
    screen.blit(top_card_text, (SCREEN_WIDTH // 2 - 150, 50)) #1