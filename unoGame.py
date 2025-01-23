import pygame
from settings import *
from unoPlayers import *
from unoCard import *
from uno import *
from unoHandleTurn import *

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
        
        pygame.draw.rect(screen, BLACK, (rect_x, rect_y, rect_width, rect_height), border_radius=10)
        pygame.draw.rect(screen, WHITE, (rect_x, rect_y, rect_width, rect_height), width=8, border_radius=10)
        oval_width, oval_height = rect_width *0.8  , rect_height * 0.7 

        logo = pygame.image.load('logo.png')  
        scaled_logo = pygame.transform.scale(logo, (int(oval_width * 0.95), int(oval_height * 0.95)))  
    
        logo_rect = scaled_logo.get_rect(center=(rect_x + rect_width // 2, rect_y + rect_height // 2))
        screen.blit(scaled_logo, logo_rect.topleft)
        
        rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
        return rect
        
           


def position_other_players(num_players,ai_players, hum_players):
    """Positions the other players dynamically based on number of players."""
    positions = []
    print(num_players, ai_players, hum_players)
    if ai_players == 1:
        positions.append((SCREEN_WIDTH // 10, SCREEN_HEIGHT - 170))   # Current players hand
        positions.append((SCREEN_WIDTH // 3, SCREEN_HEIGHT // 8)) 
    
    elif ai_players == 2:
        positions.append((SCREEN_WIDTH // 10 ,  SCREEN_HEIGHT - 170))   # Current players hand
        positions.append((50, SCREEN_HEIGHT // 4 ))  
        positions.append((SCREEN_WIDTH-180, SCREEN_HEIGHT // 4))  

    elif ai_players == 3:
        positions.append((SCREEN_WIDTH // 10 ,  SCREEN_HEIGHT - 170))   # Current players hand
        positions.append((SCREEN_WIDTH // 3, SCREEN_HEIGHT // 8 ))  
        positions.append((50, SCREEN_HEIGHT // 4))  
        positions.append((SCREEN_WIDTH - 180, SCREEN_HEIGHT // 4))  
    return positions
def show_uno_button(player):
    # Define the button properties
    button_width, button_height = 200, 50
    button_x = SCREEN_WIDTH // 2 - button_width // 2
    button_y = SCREEN_HEIGHT // 1.5 - button_height - 10
    
    # Draw the button
    pygame.draw.rect(screen, RED, (button_x, button_y, button_width, button_height), border_radius=10)
    pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height), width=5, border_radius=10)

    text = FONT_MEDIUM.render("UNO!", True, WHITE)
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(text, text_rect)

    return pygame.Rect(button_x, button_y, button_width, button_height)
def check_uno_button(current_player,deck):
    if len(current_player.hand) == 1:  
            if isinstance(current_player, AIPlayer):
                print(f"{current_player.name} calls UNO.")
            else:
                uno = input("You have one card left! Type 'UNO' to call it: ").lower()
                if uno != 'uno':
                    print(f"{current_player.name} didn't call 'UNO'! You draw 2 penalty cards.")
                    current_player.draw(deck, 2)  


def main_game():
    show_initial_screen()
    num_players = ask_number_of_players(screen, clock)
    player_types = ask_type_of_players(num_players, screen, clock)
    players = create_playerz(player_types, num_players, screen, clock)
    ai_players = [player for player in players if isinstance(player, AIPlayer)]
    hum_players = [player for player in players if not isinstance(player, AIPlayer)]
    playersAndHum =[]
    playersAndHum.append(hum_players)
    playersAndHum.append(ai_players)


    print(players,playersAndHum)
    deck = Deck()
    deck.shuffle()
    discard_pile = DiscardPile(deck)
    current_player_index = 0

    for player in players:
        player.draw(deck, 7)

    positions = position_other_players(num_players,len(ai_players), len(hum_players))
    running = True
    reverse_order = False
    stacked = 0
    ai=False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if uno_button_rect.collidepoint(mouse_pos):  
                    print("UNO! button pressed")
                    """if len(current_player.hand > 1):
                        print("oh noo")
                        current_player.draw(deck)"""
        

        screen.fill(LIGHT_BLUE)
        d_rect = display_discard_pile(discard_pile, screen)
        current_player = players[current_player_index]

        name_text = FONT_MEDIUM.render(f"Current player: {current_player.name}", True, BLACK)
        name_rect = name_text.get_rect(topleft=(10, 10))  
        screen.blit(name_text, name_rect)
        uno_button_rect = show_uno_button(current_player)

        if stacked > 0:
            active_stack_text = FONT_MEDIUM.render(f"Active stack: {stacked} cards.", True, BLACK)
            active_stack_rect = active_stack_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))  
            screen.blit(active_stack_text, active_stack_rect)

        if not isinstance(current_player, AIPlayer):
            current_player_index, reverse_order, stacked , move_completed= handle_human_turn(
                current_player, discard_pile, deck, screen, positions, current_player_index, reverse_order, stacked,ai,d_rect,players
            )
            if move_completed:
                step = -1 if reverse_order else 1
                current_player_index = (current_player_index + step) % len(players)

        else:
            current_player_index, reverse_order, stacked = handle_ai_turn(current_player, discard_pile, deck, stacked,players,current_player_index,reverse_order,ai,screen)
            step = -1 if reverse_order else 1
            current_player_index = (current_player_index + step) % len(players)



        # Display other AI players' hands
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

        # Check if the current player has won
        if len(current_player.hand) == 0:
            print(f"{current_player.name} wins!")
            break
        

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main_game()
