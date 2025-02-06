import pygame

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))

# Set up font
font = pygame.font.Font(None, 36)

# Function to draw the transparent scoreboard
def draw_scoreboard(score):
    scoreboard_surface = pygame.Surface((200, 100), pygame.SRCALPHA)
    text_surface = font.render(f'Score: {score}', True, (255, 255, 255))
    scoreboard_surface.blit(text_surface, (10, 10))
    screen.blit(scoreboard_surface, (10, 10))

# Main game loop
running = True
score = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update score (example logic)
    score += 1

    # Clear screen
    screen.fill((0, 0, 0))

    # Draw scoreboard
    draw_scoreboard(score)

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
