import pygame
import random
from constants import *
from circleshape import CircleShape


class Asteroid(CircleShape):
  
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.color = "orange"
        if radius == ASTEROID_MAX_RADIUS:
            self.color = "red"
        elif radius == ASTEROID_MIN_RADIUS:
            self.color = "yellow"
        

    def draw(self, screen):
        width = 2
        if self.radius == ASTEROID_MAX_RADIUS:
            width = 4
        if self.radius == ASTEROID_MIN_RADIUS:
            width = 0
        pygame.draw.circle(screen, self.color, self.position, self.radius, width)
        # print("Radius: ", self.radius)

    def update(self, dt):
        # Update the position based on velocity and delta time
        self.position += self.velocity * dt

        # Horizontal wrap-around:
        if self.position.x > SCREEN_WIDTH + self.radius + 1:
            self.position.x = -self.radius + 1
        elif self.position.x < -self.radius - 1:
            self.position.x = SCREEN_WIDTH + self.radius - 1

        # Vertical wrap-around:
        if self.position.y > SCREEN_HEIGHT + self.radius + 1:
            self.position.y = -self.radius + 1
        elif self.position.y < -self.radius - 1:
            self.position.y = SCREEN_HEIGHT + self.radius - 1
        
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