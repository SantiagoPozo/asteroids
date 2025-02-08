import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from info_panel import draw_main_info, draw_player_stats
 
def game_over(screen, clock, restart_callback, score):
    # Create the font for the "Game Over" message
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over!", True, (255, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100))

    # Create the font for the buttons
    button_font = pygame.font.Font(None, 50)
    play_text_default = "Play Again"
    exit_text_default = "Exit"
    play_text = button_font.render(play_text_default, True, (255, 255, 255))
    play_rect = play_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    exit_text = button_font.render(exit_text_default, True, (255, 255, 255))
    exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
    
    # Create the font for the score display
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100))
    
    current_cursor = None
    # selected_button: 0 = Play, 1 = Exit.
    selected_button = 0

    # draw the player stats
    # draw_player_stats(screen)

    # draw the main info
    # draw_main_info(screen)

    # Main loop for the game over screen
    while True:
        mouse_pos = pygame.mouse.get_pos()

        # If mouse is hovering over a button, update selection accordingly
        if play_rect.collidepoint(mouse_pos):
            selected_button = 0
        elif exit_rect.collidepoint(mouse_pos):
            selected_button = 1

        desired_cursor = pygame.SYSTEM_CURSOR_HAND if (play_rect.collidepoint(mouse_pos) or exit_rect.collidepoint(mouse_pos)) else pygame.SYSTEM_CURSOR_ARROW
        if desired_cursor != current_cursor:
            pygame.mouse.set_cursor(desired_cursor)
            current_cursor = desired_cursor
        
        # Draw the game over screen
        

        # Process keyboard events for navigation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_button = (selected_button - 1) % 2
                elif event.key == pygame.K_DOWN:
                    selected_button = (selected_button + 1) % 2
                elif event.key in {pygame.K_SPACE, pygame.K_RETURN}:
                    if selected_button == 0:
                        restart_callback()
                        return
                    elif selected_button == 1:
                        pygame.quit()
                        sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    restart_callback()
                    return
                if exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        # Render buttons with visual feedback based on keyboard selection
        if selected_button == 0:
            play_text = button_font.render(play_text_default, True, (255, 126, 20))
            exit_text = button_font.render(exit_text_default, True, (255, 255, 255))
        else:
            play_text = button_font.render(play_text_default, True, (255, 255, 255))
            exit_text = button_font.render(exit_text_default, True, (255, 126, 20))

        screen.fill("black")
        screen.blit(text, text_rect)
        screen.blit(score_text, score_rect)
        screen.blit(play_text, play_rect)
        screen.blit(exit_text, exit_rect)
        pygame.display.flip()
        clock.tick(60)
