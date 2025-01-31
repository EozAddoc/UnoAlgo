import pygame
from settings import *
from uno import *

def draw_card(screen, card, x, y, is_ai=False, rotate=False, valid=False):
    """
    Dessine une carte UNO sur l'écran.

    Paramètres:
        screen (pygame.Surface): Surface sur laquelle dessiner la carte.
        card (objet Card): Carte à dessiner.
        x (int): Position horizontale de la carte.
        y (int): Position verticale de la carte.
        is_ai (bool): Si True, affiche une carte face cachée pour l'IA.
        rotate (bool): Si True, fait pivoter la carte de 90°.
        valid (bool): Indique si la carte est un coup valide (ajoute une bordure rouge).

    Retourne:
        pygame.Rect: Rectangle correspondant à la position et taille de la carte.
    """

    # Définition des dimensions de la carte
    card_width, card_height = SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.18

    # Dictionnaire associant les couleurs UNO à des valeurs RGB
    color_map = {
        "R": (255, 0, 0),   # Rouge
        "G": (0, 255, 0),   # Vert
        "B": (0, 0, 255),   # Bleu
        "Y": (209, 209, 50),# Jaune
        "W": (128, 128, 128)# Joker (wild card)
    }

    # Création d'une surface pour dessiner la carte avec transparence
    card_surface = pygame.Surface((card_width, card_height), pygame.SRCALPHA)

    if is_ai:
        # Dessiner une carte face cachée pour l'IA
        pygame.draw.rect(card_surface, BLACK, (0, 0, card_width, card_height), border_radius=10)
        pygame.draw.rect(card_surface, WHITE, (0, 0, card_width, card_height), width=8, border_radius=10)

        # Dessin d'une ellipse rouge en fond
        ellipse_surface = pygame.Surface((card_width, card_height), pygame.SRCALPHA)
        pygame.draw.ellipse(ellipse_surface, RED, ((card_width * 0.15), (card_height * 0.1), card_width * 0.7, card_height * 0.8))
        
        # Charger et redimensionner le logo UNO
        logo = pygame.image.load('logo.png')
        scaled_png = pygame.transform.scale(logo, (int(card_width * 0.55), int(card_height * 0.55)))
        
        # Positionner le logo au centre de la carte
        png_rect = scaled_png.get_rect(center=(card_width // 2, card_height // 2))

        # Rotation de l'ellipse pour l'effet UNO
        rotated_ellipse = pygame.transform.rotate(ellipse_surface, -35)
        rotated_rect = rotated_ellipse.get_rect(center=(card_width // 2, card_height // 2))

        # Ajouter l'ellipse et le logo sur la carte
        card_surface.blit(rotated_ellipse, rotated_rect.topleft)
        card_surface.blit(scaled_png, png_rect.topleft)

    else:
        # Dessiner une carte avec sa vraie couleur
        card_color = color_map.get(card.color, BLACK)
        pygame.draw.rect(card_surface, card_color, (0, 0, card_width, card_height), border_radius=10)
        pygame.draw.rect(card_surface, WHITE, (0, 0, card_width, card_height), width=8, border_radius=10)

        # Dessiner l'ovale central blanc
        ellipse_surface = pygame.Surface((card_width, card_height), pygame.SRCALPHA)
        pygame.draw.ellipse(ellipse_surface, WHITE, ((card_width * 0.15), (card_height * 0.03), card_width * 0.7, card_height * 0.94))

        # Appliquer une rotation pour donner l'effet UNO
        rotated_ellipse = pygame.transform.rotate(ellipse_surface, -35)
        rotated_rect = rotated_ellipse.get_rect(center=(card_width // 2, card_height // 2))
        card_surface.blit(rotated_ellipse, rotated_rect.topleft)

        # Dessiner les numéros de la carte
        font_size = int(SCREEN_HEIGHT * 0.05)
        large_font_size = int(SCREEN_HEIGHT * 0.08)
        font = pygame.font.Font(None, font_size)
        large_font = pygame.font.Font(None, large_font_size)

        # Texte en haut à gauche
        text_top_left = font.render(card.value, True, WHITE)
        text_top_left_rect = text_top_left.get_rect(topleft=(10, 10))
        card_surface.blit(text_top_left, text_top_left_rect)

        # Texte principal avec effet d'ombre
        shadow_text_center = large_font.render(card.value, True, BLACK)
        shadow_rect_center = shadow_text_center.get_rect(center=(card_width // 2 + 2, card_height // 2 + 2))
        card_surface.blit(shadow_text_center, shadow_rect_center.topleft)

        text_center = large_font.render(card.value, True, card_color)
        text_center_rect = text_center.get_rect(center=(card_width // 2, card_height // 2))
        card_surface.blit(text_center, text_center_rect.topleft)

        # Texte en bas à droite
        text_bottom_right = font.render(card.value, True, WHITE)
        text_bottom_right_rect = text_bottom_right.get_rect(bottomright=(card_width - 10, card_height - 10))
        card_surface.blit(text_bottom_right, text_bottom_right_rect)

        # Ajouter une bordure rouge si la carte est un coup valide
        if valid:
            pygame.draw.rect(card_surface, RED, (0, 0, card_width, card_height), width=5, border_radius=10)

    # Rotation de la carte si nécessaire
    if rotate:
        card_surface = pygame.transform.rotate(card_surface, 90)

    # Afficher la carte sur l'écran
    screen.blit(card_surface, (x, y))

    return card_surface.get_rect(topleft=(x, y))

def draw_hand(screen, player, start_x, start_y, discard_pile, is_ai=False, rotate=True):
    """
    Dessine la main d'un joueur.

    Paramètres:
        screen (pygame.Surface): Surface de jeu.
        player (objet Player): Joueur dont on affiche la main.
        start_x (int): Position de départ en X.
        start_y (int): Position de départ en Y.
        discard_pile (objet Pile): Pile de défausse actuelle.
        is_ai (bool): Si True, la main est cachée (pour l'IA).
        rotate (bool): Si True, les cartes sont affichées verticalement.

    Retourne:
        list: Liste des rectangles des cartes pour la gestion des interactions.
    """

    spacing = SCREEN_WIDTH * 0.12  # Espacement entre les cartes pour le joueur
    spacing_others = 0.03  # Espacement pour les autres joueurs
    valid_moves = player.valid_moves(discard_pile.top_card)  # Récupération des coups valides
    card_rects = []

    if len(player.hand) > 8:
        spacing_others = 0.03  # Ajuster l'espacement si le joueur a plus de 8 cartes

    if not rotate:
        for i, card in enumerate(player.hand):
            x = draw_card(screen, card, start_x + i * SCREEN_WIDTH * (spacing if not is_ai else spacing_others), start_y, is_ai, rotate, valid=(card in valid_moves))
            card_rects.append(x)
    else:
        for i, card in enumerate(player.hand):
            draw_card(screen, card, start_x, start_y + i * SCREEN_WIDTH * spacing_others, is_ai, rotate, valid=False)

    return card_rects

def display_hand(player, screen, position, discard_pile, is_ai=False, rotate=True):
    """
    Affiche la main du joueur à une position donnée.

    Retourne:
        Liste des rectangles des cartes affichées.
    """
    return draw_hand(screen, player, position[0], position[1], discard_pile, is_ai, rotate)

def display_discard_pile(discard_pile, screen):
    """
    Affiche la carte du dessus de la pile de défausse.
    """
    font = pygame.font.SysFont('Arial', 30)
    top_card_text = font.render(f"Discard Pile: {str(discard_pile.top_card)}", True, BLACK)
    screen.blit(top_card_text, (SCREEN_WIDTH // 2 - 150, 50))
