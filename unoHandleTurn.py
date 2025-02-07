import pygame 
from settings import * 
from unoPlayers import * 
from unoCard import * 
from uno import * 
def handle_human_turn(current_player, discard_pile, deck, screen, positions, current_player_index, reverse_order, stacked, ai, d_rect, players): #76n **2 + 11 n**3 + 5n
    """
    Handles the turn of a human player in the UNO game.

    This function:
    - Displays the player's hand.
    - Handles mouse click events to play a card or draw from the deck.
    - Manages stacking rules for +2 and +4 cards.
    - Updates the game state accordingly.

    Parameters:
    -----------
    current_player : Player
        The human player whose turn is being handled.
    discard_pile : DiscardPile
        The pile where played cards are placed.
    deck : Deck
        The deck from which players draw cards.
    screen : pygame.Surface
        The Pygame display surface for rendering UI elements.
    positions : list
        List of screen positions corresponding to player hands.
    current_player_index : int
        The index of the current player in the players list.
    reverse_order : bool
        Indicates whether play order is reversed.
    stacked : int
        The number of stacked +2 or +4 cards that must be resolved.
    ai : bool
        Indicates whether AI players are present in the game.
    d_rect : pygame.Rect
        The rectangle representing the deck for click detection.
    players : list
        List of all players (human and AI).

    Returns:
    --------
    tuple
        (current_player_index, reverse_order, stacked, move_completed)
        - current_player_index (int): Updated index of the current player.
        - reverse_order (bool): Updated play order.
        - stacked (int): Updated stack count if applicable.
        - move_completed (bool): Whether the player successfully made a move.
    """
 
    card_rects = display_hand(current_player, screen, positions[current_player_index], discard_pile, is_ai=False, rotate=False) #1
    move_completed = False  # Ensure move is initially not completed #1
    for event in pygame.event.get(): #76n **2 + 11 n**3 + 5n
        if event.type == pygame.MOUSEBUTTONDOWN: #1
            x, y = event.pos #1
            if d_rect.x - 50 <= x <= d_rect.x + d_rect.width + 50 and d_rect.y - 50 <= y <= d_rect.y + d_rect.height + 50 and stacked ==0: #1
                current_player.draw(deck) #3n
                move_completed = True #1
                return current_player_index, reverse_order, stacked, move_completed #1
 
            for i, card_rect in enumerate(card_rects): #73n + 11 n**2
                clickable_rect = pygame.Rect( #1
                card_rect.x,  
                card_rect.y,  
                card_rect.width,  
                card_rect.height 
            ) 
                pygame.draw.rect(screen, YELLOW, clickable_rect, width=5) #1
                if clickable_rect.collidepoint(x, y): #1
                    card = current_player.hand[i] #1
                    valid_moves = current_player.valid_moves(discard_pile.top_card) #1
     
                    if stacked > 0: #1
                        print(f"A stack of {stacked} cards must be resolved.") #1
                        print("Your options: Play another +2 or +4 to add to the stack, or type 'draw'.")      #1
                    if stacked > 0 and card.value not in ["+2", "+4"]: #1
                        print(f"You draw {stacked} cards due to the stack!") #1
                        for _ in range(stacked): #3n**2
                            current_player.draw(deck) #3n
                        stacked = 0   #1
                        move_completed = True #1
                        return current_player_index, reverse_order, stacked, move_completed #1

                    else: 
                        if card in valid_moves: #1
                            current_player.play(card, discard_pile) #1
                            current_player_index, reverse_order, stacked = handle_special_cards( 
                                card, players, current_player_index, reverse_order, discard_pile, deck, stacked, ai 
                            ) #54 +8n
                            move_completed = True #1
                            print(f"current player {current_player.name} played {card.value , card.color} and hand is {current_player.hand}") #1
 
                            return current_player_index, reverse_order, stacked, move_completed #1
                    break #1
    return current_player_index, reverse_order, stacked, move_completed #1
 

def handle_ai_turn(current_player, discard_pile, deck, stacked,players,current_player_index,reverse_order,ai,screen): #82 +10n + 3n**2
    """
    Handles the turn of an AI player in the UNO game.

    This function:
    - Decides the AI's move based on valid cards and stacking rules.
    - Plays a card if possible, handling special card effects.
    - Draws from the deck if no valid move is available.
    - Updates the game state accordingly.

    Parameters:
    -----------
    current_player : AIPlayer
        The AI player whose turn is being handled.
    discard_pile : DiscardPile
        The pile where played cards are placed.
    deck : Deck
        The deck from which players draw cards.
    stacked : int
        The number of stacked +2 or +4 cards that must be resolved.
    players : list
        List of all players (human and AI).
    current_player_index : int
        The index of the current player in the players list.
    reverse_order : bool
        Indicates whether play order is reversed.
    ai : bool
        Indicates whether AI players are present in the game.
    screen : pygame.Surface
        The Pygame display surface for rendering UI elements.

    Returns:
    --------
    tuple
        (current_player_index, reverse_order, stacked)
        - current_player_index (int): Updated index of the current player.
        - reverse_order (bool): Updated play order.
        - stacked (int): Updated stack count if applicable.
    """
 
    move = current_player.decide_move(discard_pile.top_card, (stacked > 0)) #15 + n
    if move and (stacked == 0 or move.value in ["+2", "+4"]): #1
        current_player.play(move, discard_pile) #5
 
        current_player_index, reverse_order, stacked = handle_special_cards( 
            move, players, current_player_index, reverse_order, discard_pile, deck, stacked,ai 
        ) #54 +8n
        print(f"current player {current_player.name} played {move} and hand is {current_player.hand}") #1
 
    else: 
        if stacked == 0: #1
            x = len(current_player.hand) #1
            current_player.draw(deck) #1
            y= len(current_player.hand) #1
 
        for _ in range(stacked): #3n**2 +n
            current_player.draw(deck) #3n
            print(f"current player {current_player.name} drew new hand is {current_player.hand}") #1
        stacked = 0 #1
    return current_player_index, reverse_order, stacked #1