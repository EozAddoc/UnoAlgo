import pygame
from settings import *  # Import des paramètres globaux
from unoPlayers import *  # Import des classes et fonctions liées aux joueurs
from unoCard import *  # Import des classes et fonctions liées aux cartes
from uno import *  # Import des règles et de la logique du jeu

def handle_human_turn(current_player, discard_pile, deck, screen, positions, current_player_index, reverse_order, stacked, ai, d_rect, players):
    """
    Gère le tour du joueur humain.

    - Affiche la main du joueur.
    - Gère les clics de la souris pour jouer une carte ou piocher.
    - Applique les règles spéciales des cartes.
    
    Arguments :
    - current_player : Joueur humain en cours
    - discard_pile : Pile de défausse
    - deck : Pioche
    - screen : Fenêtre Pygame
    - positions : Positions des joueurs à l'écran
    - current_player_index : Index du joueur en cours
    - reverse_order : Sens du jeu (normal ou inversé)
    - stacked : Nombre de cartes empilées (ex. après un +2 ou +4)
    - ai : Liste des IA
    - d_rect : Rectangle de la pile de défausse (pour détecter les clics)
    - players : Liste des joueurs

    Retourne :
    - current_player_index : Nouvel index du joueur
    - reverse_order : Sens du jeu mis à jour
    - stacked : Nombre de cartes empilées mis à jour
    - move_completed : Booléen indiquant si le tour est terminé
    """
    
    # Affichage des cartes du joueur et récupération de leurs positions
    card_rects = display_hand(current_player, screen, positions[current_player_index], discard_pile, is_ai=False, rotate=False)
    move_completed = False  # Initialisation du statut du tour

    # Gestion des événements de Pygame
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:  # Détection du clic de souris
            x, y = event.pos  # Récupération des coordonnées du clic

            # Vérifie si le joueur a cliqué sur la pioche pour piocher une carte
            if d_rect.x - 100 <= x <= d_rect.x + d_rect.width + 100 and d_rect.y - 100 <= y <= d_rect.y + d_rect.height + 100 and stacked == 0:
                current_player.draw(deck)
                move_completed = True
                return current_player_index, reverse_order, stacked, move_completed

            # Vérifie si le joueur clique sur une carte pour la jouer
            for i, card_rect in enumerate(card_rects):
                if card_rect.x - 50 <= x <= card_rect.x + card_rect.width + 50 and card_rect.y - 50 <= y <= card_rect.y + card_rect.height + 50:
                    card = current_player.hand[i]  # Récupération de la carte cliquée
                    valid_moves = current_player.valid_moves(discard_pile.top_card)  # Vérification des coups valides
    
                    # Gestion du cas où un effet de pile (+2 ou +4) est actif
                    if stacked > 0:
                        print(f"A stack of {stacked} cards must be resolved.")
                        print("Your options: Play another +2 or +4 to add to the stack, or type 'draw'.")     

                    if stacked > 0 and card.value not in ["+2", "+4"]:
                        print(f"You draw {stacked} cards due to the stack!")
                        for _ in range(stacked):
                            current_player.draw(deck)
                        stacked = 0  
                        move_completed = True
                        return current_player_index, reverse_order, stacked, move_completed

                    # Si la carte est valide, le joueur peut la jouer
                    if card in valid_moves:
                        current_player.play(card, discard_pile)
                        current_player_index, reverse_order, stacked = handle_special_cards(
                            card, players, current_player_index, reverse_order, discard_pile, deck, stacked, ai
                        )
                        move_completed = True
                        print(f"current player {current_player.name} played {card.value , card.color} and hand is {current_player.hand}")

                        return current_player_index, reverse_order, stacked, move_completed

                    break  # Arrête la boucle après la sélection d'une carte

    return current_player_index, reverse_order, stacked, move_completed


def handle_ai_turn(current_player, discard_pile, deck, stacked, players, current_player_index, reverse_order, ai, screen):
    """
    Gère le tour d'une intelligence artificielle (IA).

    - L'IA choisit un mouvement en fonction des cartes disponibles.
    - Si une carte spéciale est jouée, applique les effets.
    - Gère les cas où l'IA doit piocher des cartes.

    Arguments :
    - current_player : Joueur IA en cours
    - discard_pile : Pile de défausse
    - deck : Pioche
    - stacked : Nombre de cartes empilées (ex. après un +2 ou +4)
    - players : Liste des joueurs
    - current_player_index : Index du joueur en cours
    - reverse_order : Sens du jeu (normal ou inversé)
    - ai : Liste des IA
    - screen : Fenêtre Pygame

    Retourne :
    - current_player_index : Nouvel index du joueur
    - reverse_order : Sens du jeu mis à jour
    - stacked : Nombre de cartes empilées mis à jour
    """

    # L'IA choisit son coup
    move = current_player.decide_move(discard_pile.top_card, (stacked > 0))

    # Si un mouvement est possible et que l'IA peut jouer une carte spéciale
    if move and (stacked == 0 or move.value in ["+2", "+4"]):
        current_player.play(move, discard_pile)
        current_player_index, reverse_order, stacked = handle_special_cards(
            move, players, current_player_index, reverse_order, discard_pile, deck, stacked, ai
        )
        print(f"current player {current_player.name} played {move} and hand is {current_player.hand}")

    else:
        # Si l'IA ne peut pas jouer, elle pioche une carte
        if stacked == 0:
            x = len(current_player.hand)
            current_player.draw(deck)
            y = len(current_player.hand)

            """ Code commenté : Vérifie si l'IA peut jouer la carte qu'elle vient de piocher
            valid_moves = current_player.valid_moves(discard_pile.top_card)
            if current_player.hand[-1] in valid_moves and x < y:
                current_player.play(current_player.hand[-1], discard_pile)
                current_player_index, reverse_order, stacked = handle_special_cards(
                    current_player.hand[-1], players, current_player_index, reverse_order, discard_pile, deck, stacked, ai
                )
                print(f"current player {current_player.name} played {move} and hand is {current_player.hand}")
                return current_player_index, reverse_order, stacked
            """

        # Si l'IA doit encore piocher des cartes empilées
        for _ in range(stacked):
            current_player.draw(deck)
            print(f"current player {current_player.name} drew new hand is {current_player.hand}")
        stacked = 0  # Réinitialisation du compteur de cartes empilées

    return current_player_index, reverse_order, stacked
