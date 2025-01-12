import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CARD_WIDTH = 100
CARD_HEIGHT = 150
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Card Game")

# Card class to represent a single card
class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __str__(self):
        return f"{self.value} of {self.color}"

# Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = self.generate_hand()

    def generate_hand(self):
        colors = ['Red', 'Green', 'Blue', 'Yellow']
        values = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'Skip', 'Reverse', 'Draw Two']
        return [Card(random.choice(colors), random.choice(values)) for _ in range(7)]

# Function to draw a single card on the screen
def draw_card(screen, card, x, y, rotate=0):
    card_surface = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
    card_surface.fill(WHITE)
    pygame.draw.rect(card_surface, BLACK, (0, 0, CARD_WIDTH, CARD_HEIGHT), 3)

    # Draw the card color
    color_map = {'Red': RED, 'Green': GREEN, 'Blue': BLUE, 'Yellow': YELLOW}
    pygame.draw.rect(card_surface, color_map[card.color], (0, 0, CARD_WIDTH, CARD_HEIGHT))

    # Add the value text to the card
    font = pygame.font.Font(None, 30)
    text = font.render(card.value, True, BLACK)
    text_rect = text.get_rect(center=(CARD_WIDTH // 2, CARD_HEIGHT // 2))
    card_surface.blit(text, text_rect)

    # Rotate the card if needed
    if rotate != 0:
        card_surface = pygame.transform.rotate(card_surface, rotate)

    # Blit the card onto the screen
    screen.blit(card_surface, (x, y))

# Function to draw a player's hand of cards
def draw_hand(screen, player, x, y, rotate=0):
    spacing = CARD_WIDTH + 10  # Horizontal spacing between cards
    for i, card in enumerate(player.hand):
        draw_card(screen, card, x + i * spacing, y, rotate)

# Function to display all players' hands
def display_players(players, screen):
    # Player 1 (bottom)
    player1_pos = (SCREEN_WIDTH // 2 - (len(players[0].hand) * (CARD_WIDTH + 10)) // 2, SCREEN_HEIGHT - 200)
    draw_hand(screen, players[0], player1_pos[0], player1_pos[1], rotate=0)

    # Player 4 (top - upside down)
    player4_pos = (SCREEN_WIDTH // 2 - (len(players[3].hand) * (CARD_WIDTH + 10)) // 2, 100)
    draw_hand(screen, players[3], player4_pos[0], player4_pos[1], rotate=180)

    # Player 2 (left - sideways)
    player2_pos = (100, SCREEN_HEIGHT // 2 - 50)
    draw_hand(screen, players[1], player2_pos[0], player2_pos[1], rotate=90)

    # Player 3 (right - sideways)
    player3_pos = (SCREEN_WIDTH - 100 - len(players[2].hand) * (CARD_WIDTH + 10), SCREEN_HEIGHT // 2 - 50)
    draw_hand(screen, players[2], player3_pos[0], player3_pos[1], rotate=-90)

def main():
    # Create players
    players = [Player("Player 1"), Player("Player 2"), Player("Player 3"), Player("Player 4")]

    # Main game loop
    running = True
    while running:
        screen.fill(WHITE)

        # Display players' hands
        display_players(players, screen)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update the display
        pygame.display.flip()

    # Quit pygame
    pygame.quit()

if __name__ == "__main__":
    main()
