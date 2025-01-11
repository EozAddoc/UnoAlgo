import pygame
from settings import *
from unoPlayers import *
from unoCard import *
from uno import *

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('UNO Game')
clock = pygame.time.Clock()

# Load card back image

def show_initial_screen():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 350 <= event.pos[0] <= 450 and 300 <= event.pos[1] <= 350:
                    return  # Start the next screen

        screen.fill(WHITE)
        uno_text_start = FONT_LARGE.render("UNO", True, RED)
        uno_text_start_rect = uno_text_start.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(uno_text_start, uno_text_start_rect)

        pygame.draw.rect(screen, BLUE, (350, 300, 100, 50))
        text_play = FONT_MEDIUM.render("Play", True, WHITE)
        text_play_rect = text_play.get_rect(center=(400, 325))
        screen.blit(text_play, text_play_rect)

        pygame.display.flip()
        clock.tick(60)



def display_discard_pile(discard_pile, screen, x_offset=50, y_offset=50):
    font = pygame.font.SysFont('Arial', 30)
    if discard_pile.pile:
        top_card_text = font.render(f"Top card: {discard_pile.top_card}", True, BLACK)
        screen.blit(top_card_text, (x_offset, y_offset))

def position_other_players(num_players, players):
    """Positions the other players dynamically based on number of players."""
    positions = []

    if num_players == 2:
        # One AI player: position opposite
        positions.append((SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150))  # Human player hand (bottom)
        positions.append((SCREEN_WIDTH // 2, 50))  # AI player hand (top)
    
    elif num_players == 3:
        # Two AI players: position left and right of the human player
        positions.append((SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150))  # Human player hand (bottom)
        positions.append((50, SCREEN_HEIGHT // 2))  # AI player hand (left)
        positions.append((SCREEN_WIDTH - 150, SCREEN_HEIGHT // 2))  # AI player hand (right)

    elif num_players == 4:
        # Four players: position on all sides
        positions.append((SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150))  # Human player hand (bottom)
        positions.append((SCREEN_WIDTH // 2, 50))  # AI player hand (top)
        positions.append((50, SCREEN_HEIGHT // 2))  # AI player hand (left)
        positions.append((SCREEN_WIDTH - 150, SCREEN_HEIGHT // 2))  # AI player hand (right)
    
    return positions

def main_game():
    show_initial_screen()
    num_players = ask_number_of_players(screen, clock)  # Ensure this function is defined
    player_types = ask_type_of_players(num_players, screen, clock)  # Ensure this function is defined
    players = create_playerz(player_types, num_players, screen, clock)  # Ensure create_players is updated for this signature
    
    deck = Deck()
    deck.shuffle()
    
    # Create a discard pile
    discard_pile = DiscardPile(deck)
    
    # Draw 7 cards for each player
    for player in players:
        player.draw(deck, 7)

    # Create the positions for each player
    positions = position_other_players(num_players, players)

    # Game loop (add your game logic here)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        # Display Discard Pile
        display_discard_pile(discard_pile, screen)

        # Display Human Player's Hand (always at the bottom)
        display_hand(players[0], screen, positions[0])

        # Display other players' hands (AI players with card backs)
        for i, p in enumerate(players[1:], start=1):  # Skip human player, display AI hands
            display_hand(p, screen, positions[i], is_ai=True)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main_game()
