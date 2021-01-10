from models.Sheep import *
from models.Wolf import *

rounds = 300
sheeps_count = 15
init_pos_limit = 10.0
sheep_move_dist = 0.5
wolf_move_dist = 1.0


def main():
    # init sheeps and wolf
    wolf = Wolf(wolf_move_dist)
    sheeps = []

    for i in range(sheeps_count):
        sheep = Sheep(sheep_move_dist, init_pos_limit)
        sheeps.append(sheep)
    simulation(wolf, sheeps, rounds)
    print()


def simulation(wolf, sheeps, rounds):
    for i in range(rounds):
        if get_dies_count(sheeps) == sheeps_count:
            break
        for sheep in sheeps:
            sheep.move()
        min_distance, nearest_sheep = find_nearest_sheep(wolf, sheeps)
        wolf.try_catch_sheep(nearest_sheep, min_distance)
        print("\nround_no: " + str(i+1) + "\n" + "wolf position" + str(wolf.position) + "\ndied:" + str(get_dies_count(sheeps)))


def find_nearest_sheep(wolf, sheeps):
    min_distance = distance.euclidean(wolf.position, sheeps[0].position)
    nearest_sheep = sheeps[0]
    for sheep in sheeps:
        if sheep.alive:
            dist = distance.euclidean(wolf.position, sheep.position)
            if dist < min_distance:
                min_distance = dist
                nearest_sheep = sheep
    return min_distance, nearest_sheep


def get_dies_count(sheeps):
    count = 0
    for sheep in sheeps:
        if not sheep.alive:
            count += 1
    return count


if __name__ == "__main__":
    main()
