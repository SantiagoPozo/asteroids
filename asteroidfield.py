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
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.spawn_period = ASTEROID_SPAWN_RATE
        self.size = 0
        self.spawn_special = False
        self.multiplicity = 1
        self.range_of_possibilities = 1
    def reset(self):
        self.size = 0
        self.spawn_special = False
        self.multiplicity = 1
        self.range_of_possibilities = 1
        self.spawn_timer = 0
        self.spawn_period = ASTEROID_SPAWN_RATE


    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer <= self.spawn_period:
            return
        
        self.spawn_timer > self.spawn_period
        self.spawn_timer = 0

        # spawn a new asteroid at a random edge
        for i in range(self.multiplicity):
            position, radius, velocity = self.generate_start_conditions()
            self.spawn(radius, position, velocity)

    def generate_start_conditions(self):
        edge = random.choice(self.edges)
        speed = random.randint(50, 200)
        
        position = edge[1](random.uniform(0, 1))
        kind = random.randint(1, self.range_of_possibilities)
        size_increment = 1

        if self.spawn_special:
            radius = ASTEROID_SPECIAL_RADIUS
            speed += 80
            self.spawn_special = False
        else:
            radius = ASTEROID_MIN_RADIUS * kind
            size_increment = 1
            if kind == 2: size_increment = 3
            elif kind == 3: size_increment = 7
            elif kind == 4: size_increment = 15
        
        ran = random.random()
        if radius == ASTEROID_MIN_RADIUS:    
            if ran < 0.05 * self.range_of_possibilities:
                speed += 200
            elif ran < 0.1 * self.range_of_possibilities:
                speed += 100

        velocity = edge[0] * speed
        velocity = velocity.rotate(random.randint(-30, 30))
        self.size += size_increment
        return position,radius,velocity
