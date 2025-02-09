import pygame
import random
from asteroid import Asteroid
from constants import *

class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        self.spawn_timer = 0.0
        self.spawn_period = ASTEROID_SPAWN_RATE
        self.field_size = 0
        self.spawn_special = False

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt):
        self.spawn_timer += dt
        field_size = 0


        if self.spawn_timer > self.spawn_period:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            size_increment = 1
            if self.spawn_special:
                radius = ASTEROID_SPECIAL_RADIUS
                speed += 100
                self.spawn_special = False
            else:
                radius = ASTEROID_MIN_RADIUS * kind
                size_increment = kind
                if kind == 1: size_increment = 3
                elif kind == 2: size_increment = 7
            
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            self.field_size += size_increment
            self.spawn(radius, position, velocity)
