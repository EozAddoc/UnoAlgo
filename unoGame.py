import pygame
from settings import *  # Importation des paramètres du jeu (dimensions de l'écran, couleurs, polices, etc.)
from unoPlayers import *  # Gestion des joueurs (IA et humains)
from unoCard import *  # Définition des cartes UNO
from uno import *  # Mécanismes principaux du jeu
from unoHandleTurn import *  # Gestion des tours des joueurs

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('UNO Game')
clock = pygame.time.Clock()


def show_initial_screen():
    """
    Affiche l'écran d'accueil avec un bouton "Play" pour commencer la partie.
    
    Gère les événements de fermeture de la fenêtre et le clic sur le bouton de démarrage.
    """
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Vérifie si le bouton "Play" est cliqué
                if (SCREEN_WIDTH // 2) - 50 <= event.pos[0] <= (SCREEN_WIDTH // 2) + 50 and SCREEN_HEIGHT // 1.35 - 25 <= event.pos[1] <= SCREEN_HEIGHT // 1.35:
                    return  

        screen.fill(LIGHT_BLUE)
        uno_text_start = FONT_LARGE.render("UNO", True, RED)
        uno_text_start_rect = uno_text_start.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(uno_text_start, uno_text_start_rect)

        pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 1.5, SCREEN_WIDTH // 2, SCREEN_WIDTH // 10))
        text_play = FONT_MEDIUM.render("Play", True, WHITE)
        text_play_rect = text_play.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.35))
        screen.blit(text_play, text_play_rect)

        pygame.display.flip()
        clock.tick(60)


def display_discard_pile(discard_pile, screen):
    """
    Affiche la pile de défausse avec la dernière carte jouée.
    
    Ajoute également un emplacement pour la pioche avec un logo UNO.
    """
    font = pygame.font.SysFont('Arial', 30)
    
    if discard_pile.pile:
        top_card = discard_pile.top_card
        card_x = SCREEN_WIDTH // 2.5
        card_y = SCREEN_HEIGHT // 2.5

        draw_card(screen, top_card, card_x, card_y)

        # Définition de la zone pour la pioche
        rect_x = card_x + 150
        rect_y = card_y
        rect_width = SCREEN_WIDTH * 0.1
        rect_height = SCREEN_HEIGHT * 0.18
        
        pygame.draw.rect(screen, BLACK, (rect_x, rect_y, rect_width, rect_height), border_radius=10)
        pygame.draw.rect(screen, WHITE, (rect_x, rect_y, rect_width, rect_height), width=8, border_radius=10)

        # Affichage du logo UNO sur la pioche
        logo = pygame.image.load('logo.png')
        scaled_logo = pygame.transform.scale(logo, (int(rect_width * 0.8), int(rect_height * 0.7)))
        logo_rect = scaled_logo.get_rect(center=(rect_x + rect_width // 2, rect_y + rect_height // 2))
        screen.blit(scaled_logo, logo_rect.topleft)

        return pygame.Rect(rect_x, rect_y, rect_width, rect_height)


def position_other_players(num_players, ai_players, hum_players):
    """
    Positionne dynamiquement les autres joueurs autour de la table en fonction de leur nombre.

    Retourne une liste de positions où placer les mains des joueurs.
    """
    positions = []
    if ai_players == 1:
        positions.append((SCREEN_WIDTH // 10, SCREEN_HEIGHT - 170))  # Joueur actuel
        positions.append((SCREEN_WIDTH // 3, SCREEN_HEIGHT // 8))  # IA 1

    elif ai_players == 2:
        positions.append((SCREEN_WIDTH // 10, SCREEN_HEIGHT - 170))  # Joueur actuel
        positions.append((50, SCREEN_HEIGHT // 4))  # IA 1
        positions.append((SCREEN_WIDTH - 180, SCREEN_HEIGHT // 4))  # IA 2

    elif ai_players == 3:
        positions.append((SCREEN_WIDTH // 10, SCREEN_HEIGHT - 170))  # Joueur actuel
        positions.append((SCREEN_WIDTH // 3, SCREEN_HEIGHT // 8))  # IA 1
        positions.append((50, SCREEN_HEIGHT // 4))  # IA 2
        positions.append((SCREEN_WIDTH - 180, SCREEN_HEIGHT // 4))  # IA 3

    return positions


def show_uno_button(player):
    """
    Affiche le bouton "UNO!" que le joueur peut cliquer lorsqu'il n'a plus qu'une carte.
    
    Retourne la zone du bouton pour gérer les interactions avec la souris.
    """
    button_width, button_height = 200, 50
    button_x = SCREEN_WIDTH // 2 - button_width // 2
    button_y = SCREEN_HEIGHT // 1.5 - button_height - 10

    pygame.draw.rect(screen, RED, (button_x, button_y, button_width, button_height), border_radius=10)
    pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height), width=5, border_radius=10)

    text = FONT_MEDIUM.render("UNO!", True, WHITE)
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(text, text_rect)

    return pygame.Rect(button_x, button_y, button_width, button_height)


def check_uno_button(current_player, deck):
    """
    Vérifie si le joueur a oublié d'annoncer UNO et applique une pénalité si nécessaire.
    """
    if len(current_player.hand) == 1:
        if isinstance(current_player, AIPlayer):
            print(f"{current_player.name} calls UNO.")
        else:
            uno = input("You have one card left! Type 'UNO' to call it: ").lower()
            if uno != 'uno':
                print(f"{current_player.name} didn't call 'UNO'! You draw 2 penalty cards.")
                current_player.draw(deck, 2)


def main_game():
    """
    Gère la boucle principale du jeu UNO.
    
    Initialise les joueurs, le deck, et la pile de défausse. Gère les tours et affiche les éléments graphiques.
    """
    show_initial_screen()
    num_players = ask_number_of_players(screen, clock)
    player_types = ask_type_of_players(num_players, screen, clock)
    players = create_playerz(player_types, num_players, screen, clock)

    ai_players = [player for player in players if isinstance(player, AIPlayer)]
    hum_players = [player for player in players if not isinstance(player, AIPlayer)]
    
    deck = Deck()
    deck.shuffle()
    discard_pile = DiscardPile(deck)

    current_player_index = 0
    for player in players:
        player.draw(deck, 7)

    positions = position_other_players(num_players, len(ai_players), len(hum_players))
    running = True
    reverse_order = False
    stacked = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(LIGHT_BLUE)
        display_discard_pile(discard_pile, screen)

        current_player = players[current_player_index]
        uno_button_rect = show_uno_button(current_player)

        if stacked > 0:
            active_stack_text = FONT_MEDIUM.render(f"Active stack: {stacked} cards.", True, BLACK)
            screen.blit(active_stack_text, (SCREEN_WIDTH - 200, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main_game()
