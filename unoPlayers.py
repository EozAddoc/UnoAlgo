import pygame 
from settings import * 
from uno import * 
def ask_number_of_players(screen, clock): #3 + 15n + 11n**2
    """
    Asks the user to input the number of players (between 1 and 3) using a graphical interface.

    Args:
        screen (pygame.Surface): The game screen where the input prompt is displayed.
        clock (pygame.time.Clock): The Pygame clock to regulate frame rate.
    
    Returns:
        int: The number of players selected by the user.
    """
    input_active = True #1
    user_input = "" #1
    feedback_message = "" #1
    while input_active: #15n + 11n**2
        for event in pygame.event.get(): #n11
            if event.type == pygame.QUIT: #1
                pygame.quit() #1
                exit() #1
            elif event.type == pygame.KEYDOWN: #1
                if event.key == pygame.K_RETURN: #1
                    if user_input.isdigit() and 1 <= int(user_input) <= 3 : #1
                        return int(user_input)  #1
                    else: 
                        feedback_message = "Please enter a number between 1 and 3." #1
                elif event.key == pygame.K_BACKSPACE: #1
                    user_input = user_input[:-1] #1
                else: 
                    user_input += event.unicode #1
        # Clear the screen 
        screen.fill(LIGHT_BLUE) #1
        text_1 = FONT_MEDIUM.render("How many players?", True, BLACK) #1
        text_1_rect = text_1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)) #1
        screen.blit(text_1, text_1_rect) #1
        input_box_width, input_box_height = 200, 50 #1
        pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH // 2 - input_box_width // 2, SCREEN_HEIGHT // 2, input_box_width, input_box_height), 2) #1
        text_2 = FONT_MEDIUM.render(user_input, True, BLACK) #1
        text_2_rect = text_2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + input_box_height // 2)) #1
        screen.blit(text_2, text_2_rect) #1
 
        if feedback_message: #1
            text_3 = FONT_SMALL.render(feedback_message, True, RED) #1
            text_3_rect = text_3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + input_box_height + 50)) #1
            screen.blit(text_3, text_3_rect) #1
 
        pygame.display.flip() #1
        clock.tick(60) #1

def ask_type_of_players(num, screen, clock): #12 + 33n + 28 n**2
    """
    Asks the user to select the number of human and AI players, ensuring their total matches 'num'.

    Args:
        num (int): The total number of players.
        screen (pygame.Surface): The game screen where the input prompt is displayed.
        clock (pygame.time.Clock): The Pygame clock to regulate frame rate.
    
    Returns:
        dict: A dictionary with keys 'ai' and 'hum' representing the number of AI and human players, respectively.
    """
    # Initialize variables 
    input_active = True #1
    feedback_message = "" #1
    ai_input = None #1
    hum_input = None #1
 
    ai_options = { #4
        "0": pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, 50, 50), #1
        "1": pygame.Rect(SCREEN_WIDTH // 4 + 100, SCREEN_HEIGHT // 2, 50, 50), #1
        "2": pygame.Rect(SCREEN_WIDTH // 4 + 200, SCREEN_HEIGHT // 2, 50, 50), #1
        "3": pygame.Rect(SCREEN_WIDTH // 4 + 300, SCREEN_HEIGHT // 2, 50, 50) #1
    } 
 
    hum_options = { #4
        "0": pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 100, 50, 50), #1
        "1": pygame.Rect(SCREEN_WIDTH // 4 + 100, SCREEN_HEIGHT // 2 + 100, 50, 50), #1
        "2": pygame.Rect(SCREEN_WIDTH // 4 + 200, SCREEN_HEIGHT // 2 + 100, 50, 50), #1
        "3": pygame.Rect(SCREEN_WIDTH // 4 + 300, SCREEN_HEIGHT // 2 + 100, 50, 50) #1
    } 
    while input_active: #33n + 28 n**2
        for event in pygame.event.get(): #28n
            if event.type == pygame.QUIT: #1
                pygame.quit() #1
                exit() #1
 
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click #1
                mouse_pos = pygame.mouse.get_pos() #1
 
                if ai_options["1"].collidepoint(mouse_pos): #1
                    ai_input = 1 #1
                elif ai_options["2"].collidepoint(mouse_pos): #1
                    ai_input = 2 #1
                elif ai_options["3"].collidepoint(mouse_pos): #1
                    ai_input = 3 #1
                elif ai_options["0"].collidepoint(mouse_pos): #1
                    ai_input = 0 #1
 
                # Check if the click was inside one of the Human options 
                if hum_options["1"].collidepoint(mouse_pos): #1
                    hum_input = 1 #1
                elif hum_options["2"].collidepoint(mouse_pos): #1
                    hum_input = 2 #1
                elif hum_options["3"].collidepoint(mouse_pos): #1
                    hum_input = 3 #1
                elif hum_options["0"].collidepoint(mouse_pos): #1
                    hum_input = 0 #1
 
            elif event.type == pygame.KEYDOWN: #1
                if event.key == pygame.K_RETURN: #1
                    # Validate inputs and ensure total equals 'num' #1
                    if ai_input is not None and hum_input is not None: #1
                        if ai_input + hum_input == num: #1
                            return {"ai": ai_input, "hum": hum_input} #1
                        else: 
                            feedback_message = f"Total must equal {num}. Try again." #1
                    else: 
                        feedback_message = "Please choose both AI and Human players." #1
 
        # Clear the screen 
        screen.fill(LIGHT_BLUE) #1

        # Display the question with dynamic positioning 
        text_1 = FONT_MEDIUM.render("How many of each player type?", True, BLACK) #1
        text_1_rect = text_1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)) #1
        screen.blit(text_1, text_1_rect) #1
 
        # Display AI options (1, 2, 3) #1
        font = pygame.font.SysFont('Arial', 40) #1
        option_0_text = font.render("0", True, BLACK) #1
        screen.blit(option_0_text, (ai_options["0"].x + 10, ai_options["0"].y + 10)) #1
 
        option_1_text = font.render("1", True, BLACK) #1
        screen.blit(option_1_text, (ai_options["1"].x + 10, ai_options["1"].y + 10)) #1
 
        option_2_text = font.render("2", True, BLACK) #1
        screen.blit(option_2_text, (ai_options["2"].x + 10, ai_options["2"].y + 10)) #1
 
        option_3_text = font.render("3", True, BLACK) #1
        screen.blit(option_3_text, (ai_options["3"].x + 10, ai_options["3"].y + 10)) #1
 
        option_0_text_hum = font.render("0", True, BLACK) #1
        screen.blit(option_0_text_hum, (hum_options["0"].x + 10, hum_options["0"].y + 10)) #1
 
        option_1_text_hum = font.render("1", True, BLACK) #1
        screen.blit(option_1_text_hum, (hum_options["1"].x + 10, hum_options["1"].y + 10)) #1
 
        option_2_text_hum = font.render("2", True, BLACK) #1
        screen.blit(option_2_text_hum, (hum_options["2"].x + 10, hum_options["2"].y + 10)) #1
 
        option_3_text_hum = font.render("3", True, BLACK) #1
        screen.blit(option_3_text_hum, (hum_options["3"].x + 10, hum_options["3"].y + 10)) #1
 
        # If the player clicked on one of the options, mark it as selected 
        if ai_input is not None: #1
            text = FONT_MEDIUM.render(f"AI: {ai_input}", True, BLACK) #1
            screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 4 + 100)) #1
 
        if hum_input is not None: #1
            text = FONT_MEDIUM.render(f"Humans: {hum_input}", True, BLACK) #1
            screen.blit(text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 4 + 100)) #1
 
        # Display feedback message if any 
        if feedback_message: #1
            text_3 = FONT_SMALL.render(feedback_message, True, RED) #1
            text_3_rect = text_3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)) #1
            screen.blit(text_3, text_3_rect) #1
 
        # Update the display #1
        pygame.display.flip() #1
        clock.tick(60) #1
 
def create_playerz(player_types, num, screen, clock): #10 +32n + 36n**2 +4n**3
    """
    Creates and manages the setup process for human and AI players in a Pygame-based game.

    This function handles:
    - Gathering names for human players via user input.
    - Allowing the user to select a difficulty level for AI players.
    - Creating and returning a list of Player and AIPlayer objects.

    Parameters:
    -----------
    player_types : dict
        A dictionary specifying the number of human ('hum') and AI ('ai') players.
    num : int
        Total number of players expected (both human and AI).
    screen : pygame.Surface
        The Pygame display surface where UI elements are rendered.
    clock : pygame.time.Clock
        The Pygame clock object for controlling the frame rate.

    Returns:
    --------
    list
        A list containing Player objects for human players and AIPlayer objects for AI players.
    """
    players = [] #1
    input_active = True #1
    current_name = "" #1
    player_counter = 0 #1
    ai_difficulty = None  # To store the AI difficulty selection #1
    print(player_types) #1
    
    font = pygame.font.SysFont('Arial', 30) #1
    feedback_message = "" #1
     
    # Prompt for human player names 
    while input_active: #15n + 25 n **2 + 4n**3
        screen.fill(LIGHT_BLUE) #1
 
        # Player name input #1
        if player_counter ==0: #1
            text_1 = font.render(f"Enter your name  :", True, (0, 0, 0)) #1
            screen.blit(text_1, (100, 100)) #1
        else: 
            text_1 = font.render(f"Enter name for Player {player_counter + 1} :", True, (0, 0, 0)) #1
            screen.blit(text_1, (100, 100)) #1
 
        # Input box for player name #1
        input_box_width, input_box_height = 300, 50 #1
        pygame.draw.rect(screen, (0, 0, 0), (SCREEN_WIDTH // 2 - input_box_width // 2, SCREEN_HEIGHT // 2, input_box_width, input_box_height), 2) #1
        name_text = font.render(current_name, True, (0, 0, 0)) #1
        screen.blit(name_text, (SCREEN_WIDTH // 2 - input_box_width // 2 + 10, SCREEN_HEIGHT // 2 + 10)) #1
 
        # Display feedback message if any 
        if feedback_message: #1
            feedback_text = font.render(feedback_message, True, (255, 0, 0)) #1
            screen.blit(feedback_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100)) #1
 
        # Handle events for typing name 
        for event in pygame.event.get(): #25n + 4n**2
            if event.type == pygame.QUIT: #1
                pygame.quit() #1
                exit() #1
 
            elif event.type == pygame.KEYDOWN: #1
                if event.key == pygame.K_RETURN: #1
                    if len(current_name) > 0: #1
                        players.append(Player(current_name))   #10+4n
                        current_name = ""   #1
                        player_counter += 1 #1
                        if player_counter == player_types['hum'] + 1:   #1
                            input_active = False #1
                    else: 
                        feedback_message = "Name cannot be empty." #1

                elif event.key == pygame.K_BACKSPACE: #1
                    current_name = current_name[:-1] #1
                 
                else: 
                    current_name += event.unicode #1
 
        pygame.display.flip() #1
        clock.tick(60) #1
 
    # Now, ask for a single AI difficulty #1
    while ai_difficulty is None: #15n + 11n**2
        screen.fill(LIGHT_BLUE) #1
 
        # Display difficulty options #1
        text_2 = font.render(f"Choose difficulty for AI players:", True, (0, 0, 0)) #1
        text_2_rect = text_2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)) #1
        screen.blit(text_2, text_2_rect) #1
 
        # Difficulty options (Easy, Medium, Hard) #1
        easy_text = font.render("easy", True, (0, 0, 0)) #1
        screen.blit(easy_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100)) #1
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 50), 2) #1
 
        medium_text = font.render("medium", True, (0, 0, 0)) #1
        screen.blit(medium_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)) #1
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50), 2) #1
 
        hard_text = font.render("hard", True, (0, 0, 0)) #1
        screen.blit(hard_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)) #1
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50), 2) #1
 
        # Handle events #1
        for event in pygame.event.get(): #11n
            if event.type == pygame.QUIT: #1
                pygame.quit() #1
                exit() #1
 
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click #1
                mouse_pos = pygame.mouse.get_pos() #1
                if pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 50).collidepoint(mouse_pos): #1
                    ai_difficulty = "easy" #1
                elif pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 -50, 200, 50).collidepoint(mouse_pos): #1
                    ai_difficulty = "medium" #1
                elif pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 , 200, 50).collidepoint(mouse_pos): #1
                    ai_difficulty = "hard" #1
 
        pygame.display.flip() #1
        clock.tick(60) #1
 
    # Add AI players with the selected difficulty #1
    ai_counter = 1 #1
    for _ in range(player_types['ai']): #2n
        players.append(AIPlayer(f"AI {ai_counter}", difficulty=ai_difficulty)) #19+n
        ai_counter += 1 #1
 
    return players #1