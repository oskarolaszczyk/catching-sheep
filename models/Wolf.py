from .Animal import Animal
from scipy.spatial import distance

class Wolf(Animal):
    def __init__(self, move_dist):
        super().__init__(move_dist)

    def try_catch_sheep(self, sheep, distance):

        if distance <= sheep.move_dist:
            self.set_position(sheep.position)
            sheep.die()
        else:
            x_value = (sheep.get_x() - self.get_x()) / distance
            y_value = (sheep.get_y() - self.get_y()) / distance
            self.move(x_value, y_value)

    def move(self, x, y):
        self.set_y(self.get_y() + self.move_dist * y)
        self.set_x(self.get_x() + self.move_dist * x)
