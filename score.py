import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

def draw_score(screen, score, label, position, align="left"):
    # Create a semi-transparent overlay surface
    overlay_width, overlay_height = 200, 50
    overlay = pygame.Surface((overlay_width, overlay_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 194))  # semi-transparent black

    # Create a font and render the score text in white without duplicating the colon.
    font = pygame.font.Font(None, 36)

    text = font.render(f"{label}{score}", True, (255, 255, 255))
    text_rect = text.get_rect()
    
    # Position the text inside the overlay based on alignment.
    if align == "right":
        text_rect.topright = (overlay_width - 10, 10)
    else:
        text_rect.topleft = (10, 10)
    
    overlay.blit(text, text_rect)
    # Blit the overlay onto the screen at the given position
    screen.blit(overlay, position)
