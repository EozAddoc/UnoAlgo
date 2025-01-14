import pygame
from settings import *
from uno import *
def ask_number_of_players(screen, clock):
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
        screen.fill(LIGHT_BLUE)

        text_1 = FONT_MEDIUM.render("How many players?", True, BLACK)
        text_1_rect = text_1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(text_1, text_1_rect)

        input_box_width, input_box_height = 200, 50
        pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH // 2 - input_box_width // 2, SCREEN_HEIGHT // 2, input_box_width, input_box_height), 2)
        text_2 = FONT_MEDIUM.render(user_input, True, BLACK)
        text_2_rect = text_2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + input_box_height // 2))
        screen.blit(text_2, text_2_rect)

        if feedback_message:
            text_3 = FONT_SMALL.render(feedback_message, True, RED)
            text_3_rect = text_3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + input_box_height + 50))
            screen.blit(text_3, text_3_rect)

        pygame.display.flip()
        clock.tick(60)

def ask_type_of_players(num, screen, clock):
    # Initialize variables
    input_active = True
    feedback_message = ""
    ai_input = None
    hum_input = None

    ai_options = {
        "0": pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, 50, 50),
        "1": pygame.Rect(SCREEN_WIDTH // 4 + 100, SCREEN_HEIGHT // 2, 50, 50),
        "2": pygame.Rect(SCREEN_WIDTH // 4 + 200, SCREEN_HEIGHT // 2, 50, 50),
        "3": pygame.Rect(SCREEN_WIDTH // 4 + 300, SCREEN_HEIGHT // 2, 50, 50)
    }

    hum_options = {
        "0": pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 100, 50, 50),
        "1": pygame.Rect(SCREEN_WIDTH // 4 + 100, SCREEN_HEIGHT // 2 + 100, 50, 50),
        "2": pygame.Rect(SCREEN_WIDTH // 4 + 200, SCREEN_HEIGHT // 2 + 100, 50, 50),
        "3": pygame.Rect(SCREEN_WIDTH // 4 + 300, SCREEN_HEIGHT // 2 + 100, 50, 50)
    }

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()

                if ai_options["1"].collidepoint(mouse_pos):
                    ai_input = 1
                elif ai_options["2"].collidepoint(mouse_pos):
                    ai_input = 2
                elif ai_options["3"].collidepoint(mouse_pos):
                    ai_input = 3
                elif ai_options["0"].collidepoint(mouse_pos):
                    ai_input = 0

                # Check if the click was inside one of the Human options
                if hum_options["1"].collidepoint(mouse_pos):
                    hum_input = 1
                elif hum_options["2"].collidepoint(mouse_pos):
                    hum_input = 2
                elif hum_options["3"].collidepoint(mouse_pos):
                    hum_input = 3
                elif hum_options["0"].collidepoint(mouse_pos):
                    hum_input = 0

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
        screen.fill(LIGHT_BLUE)

        # Display the question with dynamic positioning
        text_1 = FONT_MEDIUM.render("How many of each player type?", True, BLACK)
        text_1_rect = text_1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(text_1, text_1_rect)

        # Display AI options (1, 2, 3)
        font = pygame.font.SysFont('Arial', 40)
        option_0_text = font.render("0", True, BLACK)
        screen.blit(option_0_text, (ai_options["0"].x + 10, ai_options["0"].y + 10))

        option_1_text = font.render("1", True, BLACK)
        screen.blit(option_1_text, (ai_options["1"].x + 10, ai_options["1"].y + 10))

        option_2_text = font.render("2", True, BLACK)
        screen.blit(option_2_text, (ai_options["2"].x + 10, ai_options["2"].y + 10))

        option_3_text = font.render("3", True, BLACK)
        screen.blit(option_3_text, (ai_options["3"].x + 10, ai_options["3"].y + 10))

        option_0_text_hum = font.render("0", True, BLACK)
        screen.blit(option_0_text_hum, (hum_options["0"].x + 10, hum_options["0"].y + 10))

        option_1_text_hum = font.render("1", True, BLACK)
        screen.blit(option_1_text_hum, (hum_options["1"].x + 10, hum_options["1"].y + 10))

        option_2_text_hum = font.render("2", True, BLACK)
        screen.blit(option_2_text_hum, (hum_options["2"].x + 10, hum_options["2"].y + 10))

        option_3_text_hum = font.render("3", True, BLACK)
        screen.blit(option_3_text_hum, (hum_options["3"].x + 10, hum_options["3"].y + 10))

        # If the player clicked on one of the options, mark it as selected
        if ai_input is not None:
            text = FONT_MEDIUM.render(f"AI: {ai_input}", True, BLACK)
            screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 4 + 100))

        if hum_input is not None:
            text = FONT_MEDIUM.render(f"Humans: {hum_input}", True, BLACK)
            screen.blit(text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 4 + 100))

        # Display feedback message if any
        if feedback_message:
            text_3 = FONT_SMALL.render(feedback_message, True, RED)
            text_3_rect = text_3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
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
    my_name = ""
    print(player_types)
    
    font = pygame.font.SysFont('Arial', 30)
    feedback_message = ""
    
    # Prompt for human player names
    while input_active:
        screen.fill(LIGHT_BLUE)

        # Player name input
        if player_counter ==0:
            text_1 = font.render(f"Enter your name  :", True, (0, 0, 0))
            screen.blit(text_1, (100, 100))
        else:
            text_1 = font.render(f"Enter name for Player {player_counter + 1} :", True, (0, 0, 0))
            screen.blit(text_1, (100, 100))

        # Input box for player name
        input_box_width, input_box_height = 300, 50
        pygame.draw.rect(screen, (0, 0, 0), (SCREEN_WIDTH // 2 - input_box_width // 2, SCREEN_HEIGHT // 2, input_box_width, input_box_height), 2)
        name_text = font.render(current_name, True, (0, 0, 0))
        screen.blit(name_text, (SCREEN_WIDTH // 2 - input_box_width // 2 + 10, SCREEN_HEIGHT // 2 + 10))

        # Display feedback message if any
        if feedback_message:
            feedback_text = font.render(feedback_message, True, (255, 0, 0))
            screen.blit(feedback_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100))

        # Handle events for typing name
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(current_name) > 0:
                        players.append(Player(current_name))  
                        current_name = ""  
                        player_counter += 1
                        if player_counter == player_types['hum'] + 1:  
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
        screen.fill(LIGHT_BLUE)

        # Display difficulty options
        text_2 = font.render(f"Choose difficulty for AI players:", True, (0, 0, 0))
        text_2_rect = text_2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(text_2, text_2_rect)

        # Difficulty options (Easy, Medium, Hard)
        easy_text = font.render("Easy", True, (0, 0, 0))
        screen.blit(easy_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 50), 2)

        medium_text = font.render("Medium", True, (0, 0, 0))
        screen.blit(medium_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50), 2)

        hard_text = font.render("Hard", True, (0, 0, 0))
        screen.blit(hard_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50), 2)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                if pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 50).collidepoint(mouse_pos):
                    ai_difficulty = "easy"
                elif pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 -50, 200, 50).collidepoint(mouse_pos):
                    ai_difficulty = "medium"
                elif pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 , 200, 50).collidepoint(mouse_pos):
                    ai_difficulty = "hard"

        pygame.display.flip()
        clock.tick(60)

    # Add AI players with the selected difficulty
    ai_counter = 1
    for _ in range(player_types['ai']):
        players.append(AIPlayer(f"AI {ai_counter}", difficulty=ai_difficulty))
        ai_counter += 1

    return players