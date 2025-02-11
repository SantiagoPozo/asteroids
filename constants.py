# GAME
# SCREEN_WIDTH = 1280
# SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_AUMENT = SCREEN_WIDTH // 1280

LEVEL_UP = 5000 # Score
SPECIAL_UP = 10000 # Score

# COLORS
BLUE = (0, 102, 255)
PINK = (251, 0, 255)
PINK2 = (255, 100, 255)
PINK3 = (255, 200, 255)
RED_RADIOACTIVE = (255, 15, 15)
GREEN = (102, 255, 0)
PERFECT_YELLOW = (255, 255, 0)
YELLOW_VENUS = (201, 144, 0)
RED_MARS = (168, 29, 29)
GREY_PLUTONIC = (109, 105, 105)
RADIOACTIVE_GREEN = (43, 204, 35)

# ASTEROIDS 
ASTEROID_KINDS = 4
ASTEROID_MIN_RADIUS = SCREEN_WIDTH // 72 # smallest asteroid radius put 36 for very bigger
ASTEROID_MID_RADIUS = 2 * ASTEROID_MIN_RADIUS
ASTEROID_MAX_RADIUS = 3 * ASTEROID_MIN_RADIUS
ASTEROID_SUPER_RADIUS = 4 * ASTEROID_MIN_RADIUS
ASTEROID_SPECIAL_RADIUS = ASTEROID_MIN_RADIUS // 2

BASE_SCORE = {
    ASTEROID_SPECIAL_RADIUS: 800,
    ASTEROID_MIN_RADIUS: 400, 
    ASTEROID_MID_RADIUS: 200,
    ASTEROID_MAX_RADIUS: 100, 
    ASTEROID_SUPER_RADIUS: 50,
}

ASTEROIDS_COLORS = {
    ASTEROID_MIN_RADIUS: GREY_PLUTONIC,
    ASTEROID_MID_RADIUS: RED_MARS,
    ASTEROID_MAX_RADIUS: YELLOW_VENUS,
    ASTEROID_SUPER_RADIUS: (30, 130, 30),
    ASTEROID_SPECIAL_RADIUS: RADIOACTIVE_GREEN

}
ASTEROID_SPAWN_RATE = 1

# PLAYER
PLAYER_RADIUS = 50 
PLAYER_TURN_SPEED =  300        
PLAYER_SPEED = 200
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_RANGE = 1.5 * min(SCREEN_WIDTH, SCREEN_HEIGHT) 
SHIP_COLOR = "white"

# SHOTS
SHOOT_POWERUP_DURATION = 5 # seconds
SHOT_RADIUS = 5
PLAYER_SHOOT_COOLDOWN = 0.5