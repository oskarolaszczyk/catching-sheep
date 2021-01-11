class Animal:
    id_number = 0
    def __init__(self, move_dist):
        self.move_dist = move_dist
        self.position = [0.0, 0.0]

    def set_position(self, position):
        self.position = position

    def get_x(self):
        return self.position[0]

    def get_y(self):
        return self.position[1]

    def set_x(self, value):
        self.position[0] = value

    def set_y(self, value):
        self.position[1] = value
