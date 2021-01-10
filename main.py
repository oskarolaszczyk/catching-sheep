from models.Sheep import *
from models.Wolf import *
import json

rounds = 5
sheeps_count = 15
init_pos_limit = 10.0
sheep_move_dist = 0.5
wolf_move_dist = 1.0


def main():
    # init sheeps and wolf
    wolf = Wolf(wolf_move_dist)
    sheeps = []

    for i in range(sheeps_count):
        sheep = Sheep(sheep_move_dist, init_pos_limit, i+1)
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
        # json export
        json_data = create_json(sheeps, wolf, i+1)
        write_json(i+1, json_data)
        print("\nround_no: " + str(i+1) + "\n" + "wolf position" + str(wolf.position) + "\ndied:" + str(get_dies_count(sheeps)))

def find_nearest_sheep(wolf, sheeps):
    min_distance = init_pos_limit + 1000
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

def create_json(sheeps, wolf, round_no):
    x = {
        "round_no": round_no,
        "wolf_pos": {"x": wolf.get_x(),
                     "y": wolf.get_y()}
    }
    sheeps_pos = []
    for sheep in sheeps:
        if sheep.alive:
            sheeps_pos.append({
                "sheep_id": sheep.id_number,
                "sheep_pos": {"x": sheep.get_x(),
                              "y": sheep.get_y()}
                })
        else:
            sheeps_pos.append({
                "sheep_id": sheep.id_number,
                "sheep_pos": None})
    x['sheeps_pos'] = sheeps_pos

    return x


def write_json(round_no, data, filename='data/pos.json'):
    if round_no == 1:
        with open(filename,'w') as f:
            f.write(json.dumps(data, indent=5))
    else:
        with open(filename,'a') as f:
            f.write(json.dumps(data, indent=5))

if __name__ == "__main__":
    main()
