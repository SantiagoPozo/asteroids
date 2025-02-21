from constants import *

class Game:
    _instance = None  # Para implementar un singleton

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Game, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Solo se inicializa una vez
        if not hasattr(self, "initialized"):
            self.score = 0
            self.level = 0
            self.state = "running"  # "running", "game over"
            self.special_level = 0
            self.high_score = 0
            self.destroyed_asteroids = 0
            self.initialized = True
            self.asteroids_field_size = 0

    def goto_menu(self):
        self.state = "menu"

    def restart(self):
        self.score = 0
        self.level = 0
        self.state = "running"
        self.destroyed_asteroids = 0
