import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from game_over import game_over 
from info_panel import draw_main_info, draw_player_stats

def run_game(screen, clock, max_score):
    # Initialize game-specific variables and sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Player.containers = (updatable, drawable)

    asteroid_field = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    score = 0
    level = 0
    special_level = 0
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
        asteroid_field.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                if score > max_score:
                    max_score = score
                game_over(screen, clock, lambda: run_game(screen, clock, max_score), score)
                return

            for shot in shots:
                if asteroid.collides_with(shot):
                    asteroid_field.field_size -= 1
                    increment = int(asteroid.velocity.length()) + BASE_SCORE[asteroid.radius]
                    next_level_score = (level + 1) * SCORE_LEVEL_UP
                    if score < next_level_score <= score + increment:
                        level += 1

                        if asteroid_field.spawn_period > 0.001:
                            asteroid_field.spawn_period *= 0.9
                        
                        player.range += 10


                        if level == 1:
                            player.powers["double"] = 4
                            player.range /= 2
                            player.shoot_cooldown /= 0.729
                            player.powers["explosion"]["prob"] = 0.05

                        elif level == 8:
                            player.powers["double"] = 1
                            player.powers["explosion"]["prob"] = 0.1
                            player.powers["explosion"]["num"] = 5
                        elif level == 12:
                            player.powers["triple"] = 0.2
                            player.powers["explosion"]["prob"] = 0.15
                            player.powers["explosion"]["num"] = 7
                        elif level == 16:
                            player.powers["triple"] = 0.4
                            player.powers["explosion"]["prob"] = 0.2
                            player.powers["explosion"]["num"] = 11 

                        # if level % 4 == 0:
                        #     player.powers["double"] += 0.1
                        # elif level % 4 == 1:
                        #     player.powers["triple"] += 0.04
                        # elif level % 4 == 2:
                        #     player.powers["explosion"]["prob"] += 0.02
                        # else:
                        #     player.powers["explosion"]["num"] = min(20, player.powers["explosion"]["num"] + 1)


                    next_special_score = (special_level + 1) * SPECIAL_ASTEROID_APPEARS
                    if score < next_special_score <= score + increment:
                        special_level += 1
                    
                    if asteroid.radius == ASTEROID_SPECIAL_RADIUS: 
                        player.shoot_powerup_timer += SHOOT_POWERUP_DURATION
                        player.shoot_cooldown = 0.08
                        

                    score += increment
                    shot.kill()
                    asteroid.split()
                    break

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)


        # Draw the main info overlay on the top
        draw_main_info(screen, score, max_score, level)

        # Draw the player stats overlay on the top right (or wherever you prefer)
        draw_player_stats(screen, player, asteroid_field)

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
