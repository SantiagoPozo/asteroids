import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

def game_over(screen, clock, restart_callback):
    # Create the font for the "Game Over" message
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over!", True, (255, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100))

    # Create the font for the buttons
    button_font = pygame.font.Font(None, 50)
    button_text = button_font.render("Play Again", True, (255, 255, 255))
    button_rect = button_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    button_exit_text = button_font.render("Exit", True, (255, 255, 255))
    button_exit_rect = button_exit_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100))
    
    current_cursor = None

    while True:
        mouse_pos = pygame.mouse.get_pos()

        desired_cursor = pygame.SYSTEM_CURSOR_HAND if (button_rect.collidepoint(mouse_pos) or button_exit_rect.collidepoint(mouse_pos)) else pygame.SYSTEM_CURSOR_ARROW
        if desired_cursor != current_cursor:
            pygame.mouse.set_cursor(desired_cursor)
            current_cursor = desired_cursor

        if button_rect.collidepoint(mouse_pos):
            button_text = button_font.render("Play Again", True, (200, 200, 200))
        else:
            button_text = button_font.render("Play Again", True, (255, 255, 255))

        if button_exit_rect.collidepoint(mouse_pos):
            button_exit_text = button_font.render("Exit", True, (200, 200, 200))
        else:
            button_exit_text = button_font.render("Exit", True, (255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    # Call the restart callback passed as parameter
                    restart_callback()
                    return
                if button_exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        screen.fill("black")
        screen.blit(text, text_rect)
        pygame.draw.rect(screen, (0, 0, 0), button_rect.inflate(20, 20))
        screen.blit(button_text, button_rect)
        pygame.draw.rect(screen, (0, 0, 0), button_exit_rect.inflate(20, 20))
        screen.blit(button_exit_text, button_exit_rect)
        pygame.display.flip()
        clock.tick(60)
