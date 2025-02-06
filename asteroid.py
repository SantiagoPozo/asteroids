import pygame
import random
from constants import *
from circleshape import CircleShape


class Asteroid(CircleShape):
  
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt
        
    def split(self):

        self.kill()
        if self.radius > ASTEROID_MIN_RADIUS:
            angle = random.uniform(20, 50)
            v1 = self.velocity.rotate(angle)
            v2 = self.velocity.rotate(-angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            a1 = Asteroid(self.position.x, self.position.y, new_radius)
            a1.velocity = 1.2 * v1
            a2 = Asteroid(self.position.x, self.position.y, new_radius)
            a2.velocity = 1.2 * v2
        else: 
            return