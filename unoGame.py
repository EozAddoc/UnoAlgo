import pygame
from settings import *
from unoPlayers import *
from unoCard import *
from uno import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('UNO Game')
clock = pygame.time.Clock()


def show_initial_screen():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (SCREEN_WIDTH// 2) - 50 <= event.pos[0] <= (SCREEN_WIDTH// 2) +50 and SCREEN_HEIGHT//1.35 -25 <= event.pos[1] <= SCREEN_HEIGHT//1.35 -25 +25:
                    return  

        screen.fill(LIGHT_BLUE)
        uno_text_start = FONT_LARGE.render("UNO", True, RED)
        uno_text_start_rect = uno_text_start.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(uno_text_start, uno_text_start_rect)

        pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH//4, SCREEN_HEIGHT//1.5, SCREEN_WIDTH//2, SCREEN_WIDTH//10))
        text_play = FONT_MEDIUM.render("Play", True, WHITE)
        text_play_rect = text_play.get_rect(center=(SCREEN_WIDTH// 2, SCREEN_HEIGHT//1.35))
        screen.blit(text_play, text_play_rect)

        pygame.display.flip()
        clock.tick(60)

def display_discard_pile(discard_pile, screen):
    font = pygame.font.SysFont('Arial', 30)
     
    if discard_pile.pile:
        top_card = discard_pile.top_card

        card_x = SCREEN_WIDTH // 2.5
        card_y =SCREEN_HEIGHT // 2.5

        draw_card(screen, top_card, card_x, card_y)
        
        rect_x = card_x + 150
        rect_y = card_y 
        rect_width = SCREEN_WIDTH * 0.1
        rect_height =SCREEN_HEIGHT * 0.18
        
        pygame.draw.rect(screen, (100, 100, 100), (rect_x, rect_y, rect_width, rect_height), border_radius=10)
        pygame.draw.rect(screen, BLACK, (rect_x, rect_y, rect_width, rect_height), width=2, border_radius=10)

        
           


def position_other_players(num_players):
    """Positions the other players dynamically based on number of players."""
    positions = []

    if num_players == 1:
        positions.append((SCREEN_WIDTH // 10, SCREEN_HEIGHT - 170))   # Current players hand
        positions.append((SCREEN_WIDTH // 3, SCREEN_HEIGHT // 8)) 
    
    elif num_players == 2:
        positions.append((SCREEN_WIDTH // 10 ,  SCREEN_HEIGHT - 170))   # Current players hand
        positions.append((50, SCREEN_HEIGHT // 4 ))  
        positions.append((SCREEN_WIDTH-180, SCREEN_HEIGHT // 4))  

    elif num_players == 3:
        positions.append((SCREEN_WIDTH // 10 ,  SCREEN_HEIGHT - 170))   # Current players hand
        positions.append((SCREEN_WIDTH // 3, SCREEN_HEIGHT // 8 ))  
        positions.append((50, SCREEN_HEIGHT // 4))  
        positions.append((SCREEN_WIDTH - 180, SCREEN_HEIGHT // 4))  
    
    return positions

def main_game():
    show_initial_screen()
    num_players = ask_number_of_players(screen, clock)  # Ensure this function is defined
    player_types = ask_type_of_players(num_players, screen, clock)  # Ensure this function is defined
    players = create_playerz(player_types, num_players, screen, clock)  # Ensure create_players is updated for this signature

    print(players[0], player_types, num_players, players, num_players, len(players))
    deck = Deck()
    deck.shuffle()
    discard_pile = DiscardPile(deck)
    current_player_index = 0

    for player in players:
        player.draw(deck, 7)

    positions = position_other_players(num_players)
    print(positions, positions[0])
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(LIGHT_BLUE)

        display_discard_pile(discard_pile, screen)
        current_player = players[current_player_index]
        if not isinstance(current_player, AIPlayer):
            display_hand(current_player, screen, positions[current_player_index], discard_pile, is_ai=False, rotate=False)
        
        # handle turn logic
        # handle game end conditions

        # update screen with new state and wait for input
        for i, p in enumerate(players[1:], start=1):  
            if len(players) == 3:
                display_hand(p, screen, positions[i],discard_pile ,is_ai=True, rotate=True)
            elif len(players) == 4:
                if i == 2 or i == 3: 
                    display_hand(p, screen, positions[i],discard_pile ,is_ai=True, rotate=True)
                else:
                    display_hand(p, screen, positions[i],discard_pile, is_ai=True, rotate=False)
            else:
                display_hand(p, screen, positions[i],discard_pile, is_ai=True, rotate=False)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main_game()
