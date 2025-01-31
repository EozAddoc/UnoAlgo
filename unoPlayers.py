import pygame
from settings import *  # Importation des constantes et configurations du jeu
from uno import *  # Importation des classes et fonctions du jeu Uno

# Fonction pour demander le nombre de joueurs
def ask_number_of_players(screen, clock):
    input_active = True
    user_input = ""
    feedback_message = ""

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quitter le jeu proprement
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Validation de l'entrée
                    if user_input.isdigit() and 1 <= int(user_input) <= 3:
                        return int(user_input)  # Retourne le nombre de joueurs validé
                    else:
                        feedback_message = "Please enter a number between 1 and 3."
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]  # Supprimer le dernier caractère
                else:
                    user_input += event.unicode  # Ajouter la touche pressée

        # Affichage de l'écran d'entrée du nombre de joueurs
        screen.fill(LIGHT_BLUE)
        text_1 = FONT_MEDIUM.render("How many players?", True, BLACK)
        text_1_rect = text_1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(text_1, text_1_rect)

        # Boîte de saisie
        input_box_width, input_box_height = 200, 50
        pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH // 2 - input_box_width // 2, SCREEN_HEIGHT // 2, input_box_width, input_box_height), 2)
        text_2 = FONT_MEDIUM.render(user_input, True, BLACK)
        text_2_rect = text_2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + input_box_height // 2))
        screen.blit(text_2, text_2_rect)

        # Affichage du message d'erreur si applicable
        if feedback_message:
            text_3 = FONT_SMALL.render(feedback_message, True, RED)
            text_3_rect = text_3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + input_box_height + 50))
            screen.blit(text_3, text_3_rect)

        pygame.display.flip()
        clock.tick(60)
