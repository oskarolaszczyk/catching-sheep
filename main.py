from models.Sheep import *
from models.Wolf import *

init_pos_limit = 10.0
sheep_move_dist = 0.5
wolf_move_dist = 1.0

def main():
    wolf = Wolf(wolf_move_dist)
    sheep = Sheep(sheep_move_dist, init_pos_limit)

    print(wolf.position)
    print(sheep.position)


if __name__ == "__main__":
    main()

