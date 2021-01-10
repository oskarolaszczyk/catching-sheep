import random
from colorama import Fore, Style

from .Animal import Animal


class Sheep(Animal):
    def __init__(self, move_dist, init_pos_limit, id_number):
        super().__init__(move_dist)
        x = random.uniform(-init_pos_limit, init_pos_limit)
        y = random.uniform(-init_pos_limit, init_pos_limit)
        self.position = [x, y]
        self.alive = True
        self.id_number = id_number

    def move(self):
        directions = ["up", "down", "left", "right"]

        choice = random.choice(directions)

        if choice == "up":
            self.set_y(self.get_y() + self.move_dist)
        elif choice == "down":
            self.set_y(self.get_y() - self.move_dist)
        elif choice == "left":
            self.set_x(self.get_x() - self.move_dist)
        elif choice == "right":
            self.set_x(self.get_x() + self.move_dist)

    def die(self):
        self.alive = False
        print(Fore.RED + "sheep died: " + str(self.id_number), end='')
        print(Style.RESET_ALL)
