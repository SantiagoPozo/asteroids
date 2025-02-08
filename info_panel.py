import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

def draw_main_info(screen, score, max_score, level):
    """
    Draw the main info panel at the top of the screen using three columns.
    Each column displays one item: level, score, and max score.
    """
    font = pygame.font.Font(None, 24)
    items = [
        {"label": "Level", "value": level},
        {"label": "Score", "value": score},
        {"label": "Max", "value": max_score}
    ]
    column_width = SCREEN_WIDTH // 3
    top = 10
    for index, item in enumerate(items):
        text = font.render(f"{item['label']}: {item['value']}", True, (255, 255, 255))
        text_rect = text.get_rect()
        # Center the text horizontally in its column
        text_rect.centerx = index * column_width + column_width // 2
        text_rect.top = top
        screen.blit(text, text_rect)

def draw_player_stats(screen, player, asteroid_field):
    """
    Draw the player's current power-ups and range in the middle left of the screen.
    """
    font = pygame.font.Font(None, 18)
    info = [
        {"name": "Double shot", "value": player.powers["double"], "type": "float"},
        {"name": "Explosion", "value": player.powers["explosion"], "type": "float"},
        {"name": "Player range", "value": player.range, "type": "int"},
        {"name": "Asteroids rate", "value": asteroid_field.spawn_period, "type": "float"},
        {"name": "Field size", "value": asteroid_field.field_size, "type": "int"},
    ]
    title = font.render("Player Stats", True, (255, 255, 255))
    title_rect = title.get_rect(topleft=(10, SCREEN_HEIGHT // 2 - 36))
    screen.blit(title, title_rect)
    font = pygame.font.Font(None, 16)
    column_width = 100
    for index, info_item in enumerate(info):
        name_text = font.render(f"{info_item['name']}:", True, (255, 255, 255))
        if info_item["type"] == "float":
            value_text = font.render(f"{info_item['value']:.3f}", True, (255, 255, 255))
        elif info_item["type"] == "int":
            value_text = font.render(f"{info_item['value']}", True, (255, 255, 255))
        name_text_rect = name_text.get_rect(topleft=(10, SCREEN_HEIGHT // 2 - 16 + 16 * index))
        value_text_rect = value_text.get_rect(topleft=(10 + column_width, SCREEN_HEIGHT // 2 - 16 + 16 * index))
        screen.blit(name_text, name_text_rect)
        screen.blit(value_text, value_text_rect)
