import pygame
from circleshape import CircleShape
from constants import *
import random

class Shot(CircleShape):
    def __init__(self, x, y, radius, color=None):
        super().__init__(x, y, radius)
        self.distance_traveled = 0  # Counter for the distance traveled
        self.color = PINK
        self.range = PLAYER_SHOOT_RANGE

    def draw(self, screen):
        # Draw the shot using the stored self.color
        pygame.draw.circle(screen, self.color, self.position, self.radius, 0)

    def update(self, dt):
        # Calculate the distance moved this frame based on velocity and dt
        distance_this_frame = (self.velocity.length() + 1.5 * abs(self.velocity.y) ) * dt
        self.distance_traveled += distance_this_frame 

        # Update the position based on velocity and dt
        self.position += self.velocity * dt

        # If the shot has traveled beyond its allowed range, remove it
        if self.distance_traveled >= PLAYER_SHOOT_RANGE:
            self.kill()
            return

        # Wrap-around horizontally:
        if self.position.x > SCREEN_WIDTH + self.radius + 1:
            self.position.x = -self.radius - 1
        elif self.position.x < -self.radius - 1:
            self.position.x = SCREEN_WIDTH + self.radius + 1

        # Wrap-around vertically:
        if self.position.y > SCREEN_HEIGHT + self.radius + 1:
            self.position.y = -self.radius - 1
        elif self.position.y < -self.radius - 1:
            self.position.y = SCREEN_HEIGHT + self.radius + 1
