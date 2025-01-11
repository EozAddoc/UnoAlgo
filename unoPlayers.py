import pygame
from settings import *
from uno import *
def ask_number_of_players(screen,clock):
    input_active = True
    user_input = ""
    feedback_message = ""
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_input.isdigit() and 1 <= int(user_input) <= 3 :
                        return int(user_input) 
                    else:
                        feedback_message = "Please enter a number between 1 and 3."
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

        # Clear the screen
        screen.fill(WHITE)

        # Display the question
        text_1 = FONT_MEDIUM.render("How many players?", True, BLACK)
        text_1_rect = text_1.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(text_1, text_1_rect)

        # Display the input box
        pygame.draw.rect(screen, BLACK, (300, 300, 200, 50), 2)
        text_2 = FONT_MEDIUM.render(user_input, True, BLACK)
        text_2_rect = text_2.get_rect(center=(400, 325))
        screen.blit(text_2, text_2_rect)

        if feedback_message:
            text_3 = FONT_SMALL.render(feedback_message, True, RED)
            text_3_rect = text_3.get_rect(center=(SCREEN_WIDTH // 2, 400))
            screen.blit(text_3, text_3_rect)

        pygame.display.flip()
        clock.tick(60)
def ask_type_of_players(num, screen,clock):
    # Initialize variables
    input_active = True
    feedback_message = ""
    ai_input = None
    hum_input = None
    
    # Define the positions and sizes for the AI and Human options
    ai_options = {
        "1": pygame.Rect(150, 400, 50, 50),
        "2": pygame.Rect(250, 400, 50, 50),
        "3": pygame.Rect(350, 400, 50, 50)
    }
    
    hum_options = {
        "1": pygame.Rect(150, 500, 50, 50),
        "2": pygame.Rect(250, 500, 50, 50),
        "3": pygame.Rect(350, 500, 50, 50)
    }

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                
                # Check if the click was inside one of the AI options
                if ai_options["1"].collidepoint(mouse_pos):
                    ai_input = 1
                elif ai_options["2"].collidepoint(mouse_pos):
                    ai_input = 2
                elif ai_options["3"].collidepoint(mouse_pos):
                    ai_input = 3
                
                # Check if the click was inside one of the Human options
                if hum_options["1"].collidepoint(mouse_pos):
                    hum_input = 1
                elif hum_options["2"].collidepoint(mouse_pos):
                    hum_input = 2
                elif hum_options["3"].collidepoint(mouse_pos):
                    hum_input = 3

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Validate inputs and ensure total equals 'num'
                    if ai_input is not None and hum_input is not None:
                        if ai_input + hum_input == num:
                            return {"ai": ai_input, "hum": hum_input}
                        else:
                            feedback_message = f"Total must equal {num}. Try again."
                    else:
                        feedback_message = "Please choose both AI and Human players."

        # Clear the screen
        screen.fill(WHITE)

        # Display the question
        text_1 = FONT_MEDIUM.render("How many of each player type?", True, BLACK)
        text_1_rect = text_1.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(text_1, text_1_rect)

        # Display AI options (1, 2, 3)
        font = pygame.font.SysFont('Arial', 40)
        option_0_text = font.render("0", True, BLACK)
        screen.blit(option_0_text, (75, 410))

        option_1_text = font.render("1", True, BLACK)
        screen.blit(option_1_text, (175, 410))
        
        option_2_text = font.render("2", True, BLACK)
        screen.blit(option_2_text, (275, 410))
        
        option_3_text = font.render("3", True, BLACK)
        screen.blit(option_3_text, (375, 410))

        # Display Human options (1, 2, 3)
        option_0_text_hum = font.render("0", True, BLACK)
        screen.blit(option_0_text_hum, (75, 410))

        option_1_text_hum = font.render("1", True, BLACK)
        screen.blit(option_1_text_hum, (175, 510))
        
        option_2_text_hum = font.render("2", True, BLACK)
        screen.blit(option_2_text_hum, (275, 510))
        
        option_3_text_hum = font.render("3", True, BLACK)
        screen.blit(option_3_text_hum, (375, 510))

        # If the player clicked on one of the options, mark it as selected
        if ai_input is not None:
            text = FONT_MEDIUM.render(f"AI: {ai_input}", True, BLACK)
            screen.blit(text, (200, 325))
        
        if hum_input is not None:
            text = FONT_MEDIUM.render(f"Humans: {hum_input}", True, BLACK)
            screen.blit(text, (400, 325))

        # Display feedback message if any
        if feedback_message:
            text_3 = FONT_SMALL.render(feedback_message, True, RED)
            text_3_rect = text_3.get_rect(center=(SCREEN_WIDTH // 2, 450))
            screen.blit(text_3, text_3_rect)

        # Update the display
        pygame.display.flip()
        clock.tick(60)


def create_playerz(player_types, num, screen, clock):
    players = []
    input_active = True
    current_name = ""
    player_counter = 0
    ai_difficulty = None  # To store the AI difficulty selection
    
    font = pygame.font.SysFont('Arial', 30)
    feedback_message = ""
    
    # Prompt for human player names
    while input_active:
        screen.fill((255, 255, 255))

        # Player name input
        text_1 = font.render(f"Enter name for Player {player_counter + 1} :", True, (0, 0, 0))
        screen.blit(text_1, (100, 100))

        # Input box for player name
        pygame.draw.rect(screen, (0, 0, 0), (100, 150, 300, 50), 2)
        name_text = font.render(current_name, True, (0, 0, 0))
        screen.blit(name_text, (105, 155))

        # Display feedback message if any
        if feedback_message:
            feedback_text = font.render(feedback_message, True, (255, 0, 0))
            screen.blit(feedback_text, (100, 250))

        # Handle events for typing name
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(current_name) > 0:
                        players.append(Player(current_name))  # Add player to the list
                        current_name = ""  # Clear input for next player
                        player_counter += 1
                        if player_counter == player_types['hum']:  # Stop when all humans are added
                            # Now ask for AI difficulty if AI players are there
                            input_active = False
                    else:
                        feedback_message = "Name cannot be empty."
                
                elif event.key == pygame.K_BACKSPACE:
                    current_name = current_name[:-1]
                
                else:
                    current_name += event.unicode

        pygame.display.flip()
        clock.tick(60)

    # Now, ask for a single AI difficulty
    while ai_difficulty is None:
        screen.fill((255, 255, 255))

        # Display difficulty options
        text_2 = font.render(f"Choose difficulty for AI players:", True, (0, 0, 0))
        screen.blit(text_2, (100, 100))

        # Difficulty options (Easy, Medium, Hard)
        easy_text = font.render("Easy", True, (0, 0, 0))
        screen.blit(easy_text, (150, 200))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(150, 200, 200, 50), 2)

        medium_text = font.render("Medium", True, (0, 0, 0))
        screen.blit(medium_text, (150, 300))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(150, 300, 200, 50), 2)

        hard_text = font.render("Hard", True, (0, 0, 0))
        screen.blit(hard_text, (150, 400))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(150, 400, 200, 50), 2)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()

                # Check if the click was inside one of the difficulty options
                if pygame.Rect(150, 200, 200, 50).collidepoint(mouse_pos):
                    ai_difficulty = "easy"
                elif pygame.Rect(150, 300, 200, 50).collidepoint(mouse_pos):
                    ai_difficulty = "medium"
                elif pygame.Rect(150, 400, 200, 50).collidepoint(mouse_pos):
                    ai_difficulty = "hard"

        pygame.display.flip()
        clock.tick(60)

    # After selecting difficulty, create AI players with the same difficulty
    ai_counter = 1
    for player_type in player_types:
        if player_type == 'ai':
            players.append(AIPlayer(f"AI {ai_counter}", difficulty=ai_difficulty))
            ai_counter += 1

    return players
