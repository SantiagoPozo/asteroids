import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from game_over import game_over 
from score import draw_score

def run_game(screen, clock, max_score):
    # Initialize game-specific variables and sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()
    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    score = 0
    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  # Exit the game loop
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # On Escape, trigger game over menu
                    game_over(screen, clock, lambda: run_game(screen, clock, score), score)
                    return

        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                game_over(screen, clock, lambda: run_game(screen, clock, score), score)
                if score > max_score:
                    max_score = score
                return

            for shot in shots:
                if asteroid.collides_with(shot):
                    score += 200
                    if asteroid.radius == ASTEROID_MIN_RADIUS:
                        score += 300
                    elif asteroid.radius == ASTEROID_MAX_RADIUS:
                        score += 100
                    shot.kill()
                    asteroid.split()

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)

        # Draw the score overlay on the top left
        draw_score(screen, score, "score: ", (10, 10), align="left")

        # For max score, position it so the overlay is fully visible on the right side.
        draw_score(screen, max_score, "max: ", (SCREEN_WIDTH - 210, 10), align="right")


        pygame.display.flip()

        dt = clock.tick(60) / 1000

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()
    max_score = 0
    run_game(screen, clock, max_score)

if __name__ == "__main__":
    main()
