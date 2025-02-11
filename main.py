import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from info_panel import draw_main_info, draw_player_stats
from game import Game  # Nuestro objeto de estado
from levels import *

def render_button(font, label, center, is_selected):
    color = YELLOW_VENUS if is_selected else (255, 255, 255)
    surface = font.render(label, True, color)
    rect = surface.get_rect(center=center)
    return surface, rect

def run_game(screen, clock):
    # Create game state
    if "game_state" not in locals():
        game_state = Game()
    else:
        game_state.restart()

    # Initialize sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Set containers for automatic group insertion
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Player.containers = (updatable, drawable)
    AsteroidField.containers = updatable

    # Create game objects
    asteroids_field = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # Variables de control para power-ups especiales, etc.
    game_state.special_level = 0

    dt = 0
    while True:
        # Procesar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game_state.state == "running":
                        game_state.game_over()
                        asteroids_field.spawn_period = float("inf")  # Para dejar de spawnear asteroides

        # Solo actualizamos la lógica si el estado es "running"
        if game_state.state == "running":
            updatable.update(dt)

            # Procesar colisiones
            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    if game_state.score > game_state.high_score:
                        game_state.high_score = game_state.score
                    game_state.game_over()
                    asteroids_field.spawn_period = float("inf")
                    player.kill()  # Se elimina la nave
                    break  # Salir del loop de colisiones

                for shot in shots:
                    if asteroid.collides_with(shot):

                        asteroids_field.field_size -= 1
                        score_increment = int(asteroid.velocity.length()) + BASE_SCORE[asteroid.radius]
                        next_level_score = (game_state.level + 1) * LEVEL_UP

                        if game_state.score < next_level_score <= game_state.score + score_increment:
                            game_state.level += 1
                            level_up(player, game_state.level, asteroids_field)

                        next_special_score = (game_state.special_level + 1) * SPECIAL_UP + int(1000 * game_state.special_level ** 1.5)

                        if game_state.score < next_special_score <= game_state.score + score_increment:
                            game_state.special_level += 1
                            asteroids_field.spawn_special = True

                        if asteroid.radius == ASTEROID_SPECIAL_RADIUS:
                            player.shoot_powerup_timer += SHOOT_POWERUP_DURATION
                            player.shoot_powerup_factor = 1 / 2
                        else: 
                            player.shoot_powerup_factor = 1

                        game_state.score += score_increment
                        shot.kill()
                        asteroid.split()
                        break  # Para evitar procesar varias colisiones en el mismo frame

        # Dibujo de la escena: siempre se dibuja el fondo actual
        screen.fill("black")
        for obj in drawable:
            obj.draw(screen)
        draw_main_info(screen, game_state.score, game_state.high_score, game_state.level)
        draw_player_stats(screen, player, asteroids_field)
        pygame.display.flip()

        dt = clock.tick(60) / 1000

        # Si el estado es "game over", entramos en el bucle del menú
        if game_state.state == "game over":
            selected_button = 0  # 0: Play Again, 1: Exit

            # Bucle exclusivo para el menú de Game Over
            while game_state.state == "game over":
                asteroids.update(dt)
                screen.fill("black")
                for obj in asteroids:
                    obj.draw(screen)
                draw_main_info(screen, game_state.score, game_state.high_score, game_state.level)
                draw_player_stats(screen, player, asteroids_field)

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
                                break  # Salir del bucle del menú para reiniciar
                            elif selected_button == 1:
                                pygame.quit()
                                sys.exit()
                    elif event.type == pygame.MOUSEMOTION:
                        mouse_pos = event.pos
                        if (abs(mouse_pos[0] - SCREEN_WIDTH/2) < 100 and abs(mouse_pos[1] - (SCREEN_HEIGHT/2)) < 25):
                            selected_button = 0
                        elif (abs(mouse_pos[0] - SCREEN_WIDTH/2) < 100 and abs(mouse_pos[1] - (SCREEN_HEIGHT/2 + 50)) < 25):
                            selected_button = 1
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if (abs(mouse_pos[0] - SCREEN_WIDTH/2) < 100 and abs(mouse_pos[1] - (SCREEN_HEIGHT/2)) < 25):
                            game_state.restart()
                            break
                        elif (abs(mouse_pos[0] - SCREEN_WIDTH/2) < 100 and abs(mouse_pos[1] - (SCREEN_HEIGHT/2 + 50)) < 25):
                            pygame.quit()
                            sys.exit()

                # Renderizar el menú de Game Over sobre el fondo actual sin borrar la pantalla
                main_font = pygame.font.Font(None, 74)
                button_font = pygame.font.Font(None, 50)
                game_over_text = main_font.render("Game Over!", True, (255, 0, 0))
                game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 100))

                play_label = "Play Again"
                play_center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
                play_surface, play_rect = render_button(button_font, play_label, play_center, selected_button == 0)

                exit_label = "Exit"
                exit_center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50)
                exit_surface, exit_rect = render_button(button_font, exit_label, exit_center, selected_button == 1)

                
                # Dibujar un overlay semi-transparente para resaltar el menú
                overlay = pygame.Surface((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                screen.blit(overlay, (SCREEN_WIDTH  // 4, SCREEN_HEIGHT // 4))
                screen.blit(game_over_text, game_over_rect)
                screen.blit(play_surface, play_rect)
                screen.blit(exit_surface, exit_rect)
                pygame.display.flip()
                clock.tick(60)
                # Si se ha reiniciado, salimos del bucle del menú
                if game_state.state == "running":
                    break
            # Reiniciamos run_game para comenzar de nuevo
            run_game(screen, clock)
            return

def level_up(player, level, asteroids_field):
    
    if level in LEVEL_DATA:
        asteroids_field.multiplicity = LEVEL_DATA[level][0]
        asteroids_field.range_of_possibilities = LEVEL_DATA[level][5]
        asteroids_field.spawn_special = False
        
        player.powers["double"] = LEVEL_DATA[level][1]
        player.powers["triple"] = LEVEL_DATA[level][2]
        player.powers["explosion"]["prob"] = LEVEL_DATA[level][3]
        player.powers["explosion"]["num"] = LEVEL_DATA[level][4]

        player.shoot_cooldown = calculate_shoot_cooldown(level)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()
    run_game(screen, clock)

if __name__ == "__main__":
    main()
