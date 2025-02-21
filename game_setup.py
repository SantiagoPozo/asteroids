# game_setup.py
from player import Player
from asteroidfield import AsteroidField
from constants import *

def initialize_game_objects(asteroids, asteroids_field):
  for asteroid in asteroids:
    asteroid.kill()
  asteroids_field.reset()
  player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
  return {
    "player": player,
    "asteroids": asteroids,
    "asteroids_field": asteroids_field,
  }
