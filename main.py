# main.py
import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from info_panel import draw_main_info, draw_player_stats
from game import Game  # Nuestro objeto de estado
from levels import *
from game_setup import initialize_game_objects

def render_button(font, label, center, is_selected):
    color = YELLOW_VENUS if is_selected else (255, 255, 255)
    surface = font.render(label, True, color)
    rect = surface.get_rect(center=center)
    return surface, rect

def is_within_button(mouse_pos, center, width=200, height=50):
    return abs(mouse_pos[0] - center[0]) < width / 2 and abs(mouse_pos[1] - center[1]) < height / 2

def handle_events_running(game_state, asteroids_field):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and game_state.state == "running":
                game_state.goto_menu()
                asteroids_field.spawn_period = float("inf")

def process_collisions(game_state, player, asteroids, shots, asteroids_field):
    for asteroid in asteroids:
        if player.collides_with(asteroid):
            player.kill()
            # game_state.high_score = max(game_state.score, game_state.high_score)
            game_state.goto_menu()
            asteroids_field.spawn_period = float("inf")
            continue
        for shot in shots:
            if asteroid.collides_with(shot):
                asteroids_field.size -= 1
                score_increment = int(asteroid.velocity.length()) + BASE_SCORE[asteroid.radius]
                next_level_score = (game_state.level + 1) * LEVEL_UP
                if game_state.score < next_level_score <= game_state.score + score_increment:
                    game_state.level += 1
                    level_up(player, game_state.level, asteroids_field)
                next_special_score = (game_state.special_level + 1) * SPECIAL_UP + int(1000 * game_state.special_level ** 2)
                if game_state.score < next_special_score <= game_state.score + score_increment:
                    game_state.special_level += 1
                    asteroids_field.spawn_special = True
                if asteroid.radius == ASTEROID_SPECIAL_RADIUS:
                    player.shoot_powerup_timer += SHOOT_POWERUP_DURATION
                    player.shoot_powerup_factor = 1 / 2
                else:
                    player.shoot_powerup_factor = 1
                game_state.score += score_increment
                game_state.high_score = max(game_state.score, game_state.high_score)
                shot.kill()
                asteroid.split()
                break

def draw_game(screen, drawable, game_state, player, asteroids_field):
    screen.fill("black")
    for obj in drawable:
        obj.draw(screen)
    draw_main_info(screen, game_state.score, game_state.high_score, game_state.level)
    draw_player_stats(screen, player, asteroids_field)
    pygame.display.flip()

def handle_running(screen, clock, game_state, player, updatable, drawable, asteroids, shots, asteroids_field):
    dt = clock.tick(60) / 1000
    handle_events_running(game_state, asteroids_field)
    updatable.update(dt)
    process_collisions(game_state, player, asteroids, shots, asteroids_field)
    draw_game(screen, drawable, game_state, player, asteroids_field)
    return dt

def handle_menu(screen, clock, game_state, player, asteroids, asteroids_field):
    selected_button = 0  # 0: Play, 1: Exit
    while game_state.state == "menu":
        dt = clock.tick(60) / 1000
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
                        game_state.restart()
                        return initialize_game_objects(asteroids, asteroids_field)
                    elif selected_button == 1:
                        pygame.quit()
                        sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                if is_within_button(mouse_pos, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)):
                    selected_button = 0
                elif is_within_button(mouse_pos, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)):
                    selected_button = 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if is_within_button(mouse_pos, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)):
                    game_state.restart()
                    return initialize_game_objects(asteroids, asteroids_field)
                elif is_within_button(mouse_pos, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)):
                    pygame.quit()
                    sys.exit()

        asteroids.update(dt)
        screen.fill("black")
        for obj in asteroids:
            obj.draw(screen)
        draw_main_info(screen, game_state.score, game_state.high_score, game_state.level)
        draw_player_stats(screen, player, asteroids_field)
        blit_menu(screen, selected_button)
        pygame.display.flip()
    return None

def blit_menu(screen, selected_button):
    title_font = pygame.font.Font(None, 74)
    title_text = title_font.render("ASTEROIDS", True, (255, 0, 0))
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100))

    button_font = pygame.font.Font(None, 50)
    play_surface, _ = render_button(button_font, "Play", (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), selected_button == 0)
    exit_surface, _ = render_button(button_font, "Exit", (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50), selected_button == 1)

    overlay = pygame.Surface((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))

    screen.blit(overlay, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4))
    screen.blit(title_text, title_rect)
    screen.blit(play_surface, play_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))
    screen.blit(exit_surface, exit_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)))

def level_up(player, level, asteroids_field):
    if level not in LEVEL_DATA:
        return
    asteroids_field.multiplicity = LEVEL_DATA[level][0]
    asteroids_field.range_of_possibilities = LEVEL_DATA[level][5]
    asteroids_field.spawn_special = False
    player.powers["double"] = LEVEL_DATA[level][1]
    player.powers["triple"] = LEVEL_DATA[level][2]
    player.powers["explosion"]["prob"] = LEVEL_DATA[level][3]
    player.powers["explosion"]["num"] = LEVEL_DATA[level][4]
    player.shoot_cooldown = calculate_shoot_cooldown(level)

def run_game(screen, clock):
    game_state = Game()
    game_state.special_level = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Player.containers = (updatable, drawable)
    AsteroidField.containers = updatable
    
    asteroids_field = AsteroidField()

    
    new_game_objects = initialize_game_objects(asteroids, asteroids_field)
    player = new_game_objects["player"]
    asteroids_field = new_game_objects["asteroids_field"]

    while True:
        if game_state.state == "running":
            handle_running(screen, clock, game_state, player, updatable, drawable, asteroids, shots, asteroids_field)
        elif game_state.state == "menu":
            new_game_objects = handle_menu(screen, clock, game_state, player, asteroids, asteroids_field)
            # Si se reinició el juego, actualizamos las variables globales:
            if new_game_objects is not None:
                player = new_game_objects["player"]
                asteroids_field = new_game_objects["asteroids_field"]

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Asteroids!")
    clock = pygame.time.Clock()
    run_game(screen, clock)

if __name__ == "__main__":
    main()
