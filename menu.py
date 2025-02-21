import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, YELLOW_VENUS

def render_button(font, label, center, is_selected):
    """
    Renders a button label using the provided font.
    If is_selected is True, the label is rendered in a highlighted color.
    """
    color = YELLOW_VENUS if is_selected else (255, 255, 255)
    surface = font.render(label, True, color)
    rect = surface.get_rect(center=center)
    return surface, rect

def draw_game_over_menu(screen, score, selected_button):
    """
    Draws the Game Over menu overlay on top of the current background.
    It displays:
      - "Game Over!" at the top center.
      - The player's score.
      - Two buttons: "Play Again" and "Exit", arranged vertically.
    The parameter selected_button (0 or 1) indica cuál botón está seleccionado.
    """
    # Create fonts
    main_font = pygame.font.Font(None, 74)
    button_font = pygame.font.Font(None, 50)
    score_font = pygame.font.Font(None, 36)

    # Render static texts
    game_over_text = main_font.render("Game Over!", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100))

    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100))

    # Define button labels and centers
    play_label = "Play Again"
    exit_label = "Exit"
    play_center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    exit_center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)

    # Render the buttons based on the current selection
    play_surface, play_rect = render_button(button_font, play_label, play_center, selected_button == 0)
    exit_surface, exit_rect = render_button(button_font, exit_label, exit_center, selected_button == 1)

    # Instead of clearing the entire screen, draw a semi-transparent overlay over the current background
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))  # Black with 150 alpha
    screen.blit(overlay, (0, 0))

    # Blit the texts and buttons over the overlay
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    screen.blit(play_surface, play_rect)
    screen.blit(exit_surface, exit_rect)
