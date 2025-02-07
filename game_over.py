import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

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
    
    # Create a font for the score
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100))
    
    current_cursor = None

    while True:
        mouse_pos = pygame.mouse.get_pos()

        desired_cursor = pygame.SYSTEM_CURSOR_HAND if (play_rect.collidepoint(mouse_pos) or exit_rect.collidepoint(mouse_pos)) else pygame.SYSTEM_CURSOR_ARROW
        if desired_cursor != current_cursor:
            pygame.mouse.set_cursor(desired_cursor)
            current_cursor = desired_cursor

        # Render buttons with hover effect
        if play_rect.collidepoint(mouse_pos):
            play_text = button_font.render(play_text_default, True, (200, 200, 200))
        else:
            play_text = button_font.render(play_text_default, True, (255, 255, 255))

        if exit_rect.collidepoint(mouse_pos):
            exit_text = button_font.render(exit_text_default, True, (200, 200, 200))
        else:
            exit_text = button_font.render(exit_text_default, True, (255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    restart_callback()
                    return
                if exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        screen.fill("black")
        screen.blit(text, text_rect)
        # Draw the score text
        screen.blit(score_text, score_rect)
        # Draw buttons
        screen.blit(play_text, play_rect)
        screen.blit(exit_text, exit_rect)
        pygame.display.flip()
        clock.tick(60)
