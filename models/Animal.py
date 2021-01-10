class Animal:
    def __init__(self, move_dist):
        self.move_dist = move_dist
        self.position = [0.0, 0.0]

    def set_position(self, position):
        self.position = position
