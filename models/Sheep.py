import random
from .Animal import Animal

class Sheep(Animal):
    def __init__(self, move_dist, init_pos_limit):
        super().__init__(move_dist)
        x = random.uniform(-init_pos_limit, init_pos_limit)
        y = random.uniform(-init_pos_limit, init_pos_limit)
        self.position = [x, y]