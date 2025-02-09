import pygame
from constants import *
import random
from circleshape import CircleShape
from shot import Shot
from game_over import game_over

class Player(CircleShape):
    
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
        self.shoot_powerup_timer = 0
        self.range = PLAYER_SHOOT_RANGE
        self.powers = {
            "double": 0,
            "triple": 0,
            "explosion": {
                "prob": 0,
                "range": 0.5 * PLAYER_SHOOT_RANGE,
                "num": 3
            },
        }



    def draw(self, screen):
        color = SHIP_COLOR
        width = 1
        if self.shoot_powerup_timer > 0:
            color = RADIOACTIVE_GREEN
            width = 0
        pygame.draw.polygon(screen, color, self.ship(), width)

    def ship(self):
        points = []
        a = self.rotation
        r = self.radius
        angle_radius = [
            (a, 1.1 * r),
            (a + 100, 0.1 * r),
            (a + 60, 0.6 * r),
            (a + 150, 0.9 * r),
            (a + 160, 0.6 * r),
            (a + 180, 0.8 * r),
            (a + 200, 0.6 * r),
            (a + 210, 0.9 * r),
            (a + 300, 0.6 * r),
            (a + 260, 0.1 * r)
        ]
        for angle, radius in angle_radius:
            point = pygame.Vector2(0, 1).rotate(angle) * radius + self.position
            points.append(point)
        return points

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.timer -= dt

        # Decrease power-up timer if active
        if self.shoot_powerup_timer > 0:
            self.shoot_powerup_timer -= dt
            if self.shoot_powerup_timer <= 0:
                # Power-up expired, restore normal shooting cooldown
                self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(-dt)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_SPACE]:
            return self.shoot()

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        # Calculate forward movement based on current rotation
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

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

    def shoot(self):
        if self.timer > 0:
            return None
        
        multiple_shot = random.random()
        if multiple_shot <= self.powers["explosion"]["prob"]:
            return self.explosion_shoot()
        elif multiple_shot <= self.powers["triple"]:
            return self.triple_shoot()
        elif multiple_shot <= self.powers["double"]:
            return self.double_shoot()


        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        position = self.position + forward * self.radius
        shot = Shot(position.x, position.y, SHOT_RADIUS)
        shot.velocity = forward * PLAYER_SHOOT_SPEED
        self.timer = self.shoot_cooldown
        return shot

    def double_shoot(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        position = self.position + forward * self.radius
        shot1 = Shot(position.x, position.y, SHOT_RADIUS)
        shot2 = Shot(position.x, position.y, SHOT_RADIUS)
        shot1.range = 0.8 * self.range
        shot2.range = 0.8 * self.range
        shot1.color = PINK2
        shot2.color = PINK2
        shot1.velocity = forward.rotate(5) * PLAYER_SHOOT_SPEED
        shot2.velocity = forward.rotate(-5) * PLAYER_SHOOT_SPEED
        self.timer = self.shoot_cooldown
        return shot1, shot2
    
    def triple_shoot(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        position = self.position + forward * self.radius
        shot1 = Shot(position.x, position.y, SHOT_RADIUS)
        shot2 = Shot(position.x, position.y, SHOT_RADIUS)
        shot3 = Shot(position.x, position.y, SHOT_RADIUS)
        shot1.range = 0.6 * self.range
        shot2.range = 0.6 * self.range
        shot3.range = 0.6 * self.range
        shot1.color = PINK3
        shot2.color = PINK3
        shot3.color = PINK3
        shot1.velocity = forward.rotate(10) * PLAYER_SHOOT_SPEED
        shot2.velocity = forward * PLAYER_SHOOT_SPEED
        shot3.velocity = forward.rotate(-10) * PLAYER_SHOOT_SPEED
        self.timer = self.shoot_cooldown
        return shot1, shot2, shot3

    def explosion_shoot(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        position = self.position + forward * self.radius
        shots = []
        r = PLAYER_RADIUS
        for i in range(0, 360, 360 // self.powers["explosion"]["num"]):
            shot = Shot(position.x - r // 2, position.y - r // 2 , SHOT_RADIUS)
            shot.velocity = forward.rotate(i) * PLAYER_SHOOT_SPEED
            shots.append(shot)
        self.timer = self.shoot_cooldown
        return shots