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
            if d_rect.x - 50 <= x <= d_rect.x + d_rect.width + 50 and d_rect.y - 50 <= y <= d_rect.y + d_rect.height + 50:
                current_player.draw(deck)
                move_completed = True
                return current_player_index, reverse_order, stacked, move_completed


            for i, card_rect in enumerate(card_rects):
                if card_rect.x - 50 <= x <= card_rect.x + card_rect.width + 50 and card_rect.y - 50 <= y <= card_rect.y + card_rect.height + 50:
                    card = current_player.hand[i]
                    valid_moves = current_player.valid_moves(discard_pile.top_card)
                    if card in valid_moves:
                        current_player.play(card, discard_pile)
                        current_player_index, reverse_order, stacked = handle_special_cards(
                            card, players, current_player_index, reverse_order, discard_pile, deck, stacked, ai
                        )
                        move_completed = True
                        return current_player_index, reverse_order, stacked, move_completed

                    break
    return current_player_index, reverse_order, stacked, move_completed


def handle_ai_turn(current_player, discard_pile, deck, stacked,players,current_player_index,reverse_order,ai):
    move = current_player.decide_move(discard_pile.top_card, (stacked > 0))
    if move and (stacked == 0 or move.value in ["+2", "+4"]):
        current_player.play(move, discard_pile)
        current_player_index, reverse_order, stacked = handle_special_cards(
            move, players, current_player_index, reverse_order, discard_pile, deck, stacked,ai
        )
    else:
        if stacked == 0:
            current_player.draw(deck)
            valid_moves = current_player.valid_moves(discard_pile.top_card)
            if current_player.hand[-1] in valid_moves:
                current_player.play(current_player.hand[-1], discard_pile)
                current_player_index, reverse_order, stacked = handle_special_cards(
                    current_player.hand[-1], players, current_player_index, reverse_order, discard_pile, deck, stacked,ai
                )
        for _ in range(stacked):
            current_player.draw(deck)
        stacked = 0
    return current_player_index, reverse_order, stacked