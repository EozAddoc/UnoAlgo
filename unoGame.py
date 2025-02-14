import pygame 
from settings import *
from unoPlayers import * 
from unoCard import * 
from uno import * 
from unoHandleTurn import * 
 
pygame.init() #1
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #1
pygame.display.set_caption('UNO Game') #1
clock = pygame.time.Clock() #1
 
# Load the background image 
background = pygame.image.load("cas2.jpg")   #1

# Resize the background image to fit the screen (if needed) 
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)) #1

def show_initial_screen(): #6n**2 + 10n +1
    running = True #1
    while running: #6n**2 + 10n
        for event in pygame.event.get(): #n(6)
            if event.type == pygame.QUIT: #1
                pygame.quit() #1
                exit() #1
            elif event.type == pygame.MOUSEBUTTONDOWN: #1
                if (SCREEN_WIDTH// 2) - 50 <= event.pos[0] <= (SCREEN_WIDTH// 2) +50 and SCREEN_HEIGHT//1.35 -25 <= event.pos[1] <= SCREEN_HEIGHT//1.35 -25 +25: #1
                    return   #1
 
        screen.fill(LIGHT_BLUE) #1
        uno_text_start = FONT_LARGE.render("UNO", True, RED) #1
        uno_text_start_rect = uno_text_start.get_rect(center=(SCREEN_WIDTH // 2, 200)) #1
        screen.blit(uno_text_start, uno_text_start_rect) #1
 
        pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH//4, SCREEN_HEIGHT//1.5, SCREEN_WIDTH//2, SCREEN_WIDTH//10)) #1
        text_play = FONT_MEDIUM.render("Play", True, WHITE) #1
        text_play_rect = text_play.get_rect(center=(SCREEN_WIDTH// 2, SCREEN_HEIGHT//1.35)) #1
        screen.blit(text_play, text_play_rect) #1
 
        pygame.display.flip() #1
        clock.tick(60) #1
 
def display_discard_pile(discard_pile, screen): #74
    font = pygame.font.SysFont('Arial', 30) #1
      
    if discard_pile.pile: #1
        top_card = discard_pile.top_card #1
 
        card_x = SCREEN_WIDTH // 2.5 #1
        card_y =SCREEN_HEIGHT // 2.5 #1
 
        draw_card(screen, top_card, card_x, card_y)#56
         
        rect_x = card_x + 150 #1
        rect_y = card_y  #1
        rect_width = SCREEN_WIDTH * 0.1 #1
        rect_height =SCREEN_HEIGHT * 0.18 #1
         
        pygame.draw.rect(screen, BLACK, (rect_x, rect_y, rect_width, rect_height), border_radius=10) #1
        pygame.draw.rect(screen, WHITE, (rect_x, rect_y, rect_width, rect_height), width=8, border_radius=10) #1
        oval_width, oval_height = rect_width *0.8  , rect_height * 0.7  #1
 
        logo = pygame.image.load('logo.png')   #1
        scaled_logo = pygame.transform.scale(logo, (int(oval_width * 0.95), int(oval_height * 0.95)))   #1
     
        logo_rect = scaled_logo.get_rect(center=(rect_x + rect_width // 2, rect_y + rect_height // 2)) #1
        screen.blit(scaled_logo, logo_rect.topleft) #1
         
        rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height) #1
        return rect #1
         
            

def position_other_players(num_players,ai_players, hum_players): #15
    """Positions the other players dynamically based on number of players.""" 
    positions = [] #1
    print(num_players, ai_players, hum_players) #1
    if num_players == 1: #1
        positions.append((SCREEN_WIDTH // 10, SCREEN_HEIGHT - 170))   # Current players hand #1
        positions.append((SCREEN_WIDTH // 3, SCREEN_HEIGHT // 8))  #1
     
    elif num_players == 2: #1
        positions.append((SCREEN_WIDTH // 10 ,  SCREEN_HEIGHT - 170))   # Current players hand #1
        positions.append((50, SCREEN_HEIGHT // 4 ))   #1
        positions.append((SCREEN_WIDTH-180, SCREEN_HEIGHT // 4))   #1

    elif num_players == 3: #1
        positions.append((SCREEN_WIDTH // 10 ,  SCREEN_HEIGHT - 170))   # Current players hand #1
        positions.append((SCREEN_WIDTH // 3, SCREEN_HEIGHT // 8 ))   #1
        positions.append((50, SCREEN_HEIGHT // 4))   #1
        positions.append((SCREEN_WIDTH - 180, SCREEN_HEIGHT // 4))   #1
    return positions #1

def show_uno_button(player): #9
    # Define the button properties 
    button_width, button_height = 200, 50 #1
    button_x = SCREEN_WIDTH // 2 - button_width // 2 #1
    button_y = SCREEN_HEIGHT // 1.5 - button_height - 10 #1
    
    # Draw the button 
    pygame.draw.rect(screen, RED, (button_x, button_y, button_width, button_height), border_radius=10) #1
    pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height), width=5, border_radius=10) #1
 
    text = FONT_MEDIUM.render("UNO!", True, WHITE) #1
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2)) #1
    screen.blit(text, text_rect) #1
 
    return pygame.Rect(button_x, button_y, button_width, button_height) #1
def check_uno_button(current_player,deck): #7
    if len(current_player.hand) == 1:   #1
            if isinstance(current_player, AIPlayer): #1
                print(f"{current_player.name} calls UNO.") #1
            else: #1
                uno = input("You have one card left! Type 'UNO' to call it: ").lower() #1
                if uno != 'uno': #1
                    print(f"{current_player.name} didn't call 'UNO'! You draw 2 penalty cards.") #1
                    current_player.draw(deck, 2)   #1

def main_game(): #11n**4+115n**3+147n**2+203n+34
    show_initial_screen()  #6n**2 + 10n +1
    num_players = ask_number_of_players(screen, clock)#3 + 15n + 11n**2
    player_types = ask_type_of_players(num_players, screen, clock)  #12 + 33n + 28 n**2
    players = create_playerz(player_types, num_players, screen, clock)#10 +32n + 36n**2 +4n**3
    ai_players = [player for player in players if isinstance(player, AIPlayer)] #1
    hum_players = [player for player in players if not isinstance(player, AIPlayer)] #1
    playersAndHum =[] #1
    playersAndHum.append(hum_players) #1
    playersAndHum.append(ai_players) #1
 
    deck = Deck() #8 + 2n + 2n**2 
    deck.shuffle() #1
    discard_pile = DiscardPile(deck) #1
    current_player_index = 0 #1
    for player in players: #2n
        player.draw(deck, 7) #2
 
    positions = position_other_players(num_players,len(ai_players), len(hum_players))  #15
    running = True #1
    reverse_order = False #1
    stacked = 0 #1
    ai=False #1

    while running: #22n +6n**2 + n(43n + 32 n**2) + n(82 +10n + 3n**2) + n(76n **2 + 11 n**3 + 5n)
        for event in pygame.event.get(): #6n
            if event.type == pygame.QUIT: #1
                running = False #1
            if event.type == pygame.MOUSEBUTTONDOWN: #1
                mouse_pos = pygame.mouse.get_pos() #1
                if uno_button_rect.collidepoint(mouse_pos):   #1
                    print("UNO! button pressed") #1
        
        screen.blit(background, (0, 0))  # Draw the background at the top-left corner (0, 0) #1
        d_rect = display_discard_pile(discard_pile, screen) #1
        current_player = players[current_player_index] #1
 
        name_text = FONT_MEDIUM.render(f"Current player: {current_player.name}", True, WHITE) #1
        name_rect = name_text.get_rect(topleft=(10, 10))   #1
        screen.blit(name_text, name_rect) #1
        uno_button_rect = show_uno_button(current_player) #1
       
 
        if stacked > 0: #1
            active_stack_text = FONT_MEDIUM.render(f"Active stack: {stacked} cards.", True, WHITE) #1
            active_stack_rect = active_stack_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))   #1
            screen.blit(active_stack_text, active_stack_rect) #1
 
        if not isinstance(current_player, AIPlayer): #1
            current_player_index, reverse_order, stacked , move_completed= handle_human_turn( 
                current_player, discard_pile, deck, screen, positions, current_player_index, reverse_order, stacked,ai,d_rect,players 
            )  #76n **2 + 11 n**3 + 5n
            if move_completed: #1
                step = -1 if reverse_order else 1 #1
                current_player_index = (current_player_index + step) % len(players) #1
 
        else: 
            current_player_index, reverse_order, stacked = handle_ai_turn(current_player, discard_pile, deck, stacked,players,current_player_index,reverse_order,ai,screen) #82 +10n + 3n**2
            step = -1 if reverse_order else 1 #1
            current_player_index = (current_player_index + step) % len(players) #1

        # Display other AI players' hands #1
        for i, p in enumerate(players[1:], start=1):#43n + 32 n**2
            if len(players) == 3: #1
                display_hand(p, screen, positions[i],discard_pile ,is_ai=True, rotate=True) #10 +8n
            elif len(players) == 4: #1
                if i == 2 or i == 3:  #1
                    display_hand(p, screen, positions[i],discard_pile ,is_ai=True, rotate=True)#10 +8n
                else: 
                    display_hand(p, screen, positions[i],discard_pile, is_ai=True, rotate=False)#10 +8n
            else: 
                display_hand(p, screen, positions[i],discard_pile, is_ai=True, rotate=False) #10 +8n
 
        # Check if the current player has won #1
        if len(current_player.hand) == 0: #1
            print(f"{current_player.name} wins!") #1
            break #1
         
 
        pygame.display.flip() #1
        clock.tick(60) #1
 
    pygame.quit() #1

if __name__ == "__main__": #1
    main_game() #11n**4+115n**3+147n**2+203n+34

#Complexité est #11n**4+115n**3+147n**2+203n+34 donc O(n**4)
"""
UNO Game using Pygame

This script implements a digital version of the classic UNO card game using Pygame.  
It initializes the game environment, displays the main menu, manages player turns,  
and handles game logic for both human and AI players.

Modules Imported:
- pygame: Handles the graphical user interface.
- settings: Contains global constants (e.g., screen size, colors, fonts).
- unoPlayers: Defines player types (human and AI) and their actions.
- unoCard: Defines card properties and rendering.
- uno: Manages the game deck and discard pile.
- unoHandleTurn: Implements turn mechanics for human and AI players.

Main Components:
1. `show_initial_screen()`: Displays the start screen with a play button.
2. `display_discard_pile(discard_pile, screen)`: Renders the top card of the discard pile.
3. `position_other_players(num_players, ai_players, hum_players)`: Dynamically positions players on the screen.
4. `show_uno_button(player)`: Displays the "UNO!" button when a player has one card left.
5. `check_uno_button(current_player, deck)`: Checks if a player correctly calls "UNO!".
6. `main_game()`: Runs the main game loop, managing player turns, rendering the screen, and handling game logic.

Complexity Analysis:
- The overall time complexity is **O(n⁴)** due to nested loops and function calls.

Execution:
- Run this script to start the UNO game.
"""
