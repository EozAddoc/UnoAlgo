import pygame
from settings import *
from unoPlayers import *
from unoCard import *
from uno import *

def handle_human_turn(current_player, discard_pile, deck, screen, positions, current_player_index, reverse_order, stacked, ai, d_rect, players):

    card_rects = display_hand(current_player, screen, positions[current_player_index], discard_pile, is_ai=False, rotate=False)
    move_completed = False  # Ensure move is initially not completed
    for event in pygame.event.get():
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if d_rect.x - 100 <= x <= d_rect.x + d_rect.width + 100 and d_rect.y - 100 <= y <= d_rect.y + d_rect.height + 100 and stacked ==0:
                current_player.draw(deck)
                move_completed = True
                return current_player_index, reverse_order, stacked, move_completed


            for i, card_rect in enumerate(card_rects):
                if card_rect.x - 50 <= x <= card_rect.x + card_rect.width + 50 and card_rect.y - 50 <= y <= card_rect.y + card_rect.height + 50:
                    card = current_player.hand[i]
                    valid_moves = current_player.valid_moves(discard_pile.top_card)
    
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

                    else:
                        if card in valid_moves:
                            current_player.play(card, discard_pile)
                            current_player_index, reverse_order, stacked = handle_special_cards(
                                card, players, current_player_index, reverse_order, discard_pile, deck, stacked, ai
                            )
                            move_completed = True
                            print(f"current player {current_player.name} played {card.value , card.color} and hand is {current_player.hand}")

                            return current_player_index, reverse_order, stacked, move_completed

                    break
    return current_player_index, reverse_order, stacked, move_completed


def handle_ai_turn(current_player, discard_pile, deck, stacked,players,current_player_index,reverse_order,ai,screen):

    move = current_player.decide_move(discard_pile.top_card, (stacked > 0))
    if move and (stacked == 0 or move.value in ["+2", "+4"]):
        current_player.play(move, discard_pile)
        current_player_index, reverse_order, stacked = handle_special_cards(
            move, players, current_player_index, reverse_order, discard_pile, deck, stacked,ai
        )
        print(f"current player {current_player.name} played {move} and hand is {current_player.hand}")

    else:
        if stacked == 0:
            x = len(current_player.hand)
            current_player.draw(deck)
            y= len(current_player.hand)

            """print(current_player.hand, current_player.hand[-1],x,y)
            valid_moves = current_player.valid_moves(discard_pile.top_card)
            if current_player.hand[-1] in valid_moves and x <y:
                print("the redraw case ")
                current_player.play(current_player.hand[-1], discard_pile)
                current_player_index, reverse_order, stacked = handle_special_cards(
                    current_player.hand[-1], players, current_player_index, reverse_order, discard_pile, deck, stacked,ai
                )
                print(f"current player {current_player.name} played {move} and hand is {current_player.hand}")
                return current_player_index, reverse_order, stacked"""

        for _ in range(stacked):
            current_player.draw(deck)
            print(f"current player {current_player.name} drew new hand is {current_player.hand}")
        stacked = 0

    return current_player_index, reverse_order, stacked