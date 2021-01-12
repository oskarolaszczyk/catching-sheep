class Animal:

    def __init__(self, move_dist):
        self.move_dist = move_dist
        self.__position = [0.0, 0.0]

    def set_position(self, position):
        self.__position = position

    def get_position(self):
        return self.__position

    def get_x(self):
        return self.__position[0]

    def get_y(self):
        return self.__position[1]

    def set_x(self, value):
        self.__position[0] = value

    def set_y(self, value):
        self.__position[1] = value
