import os
import sys
import json
import csv
import logger
from models.Sheep import *
from models.Wolf import *
from config import args_parser
from data import config_file
from colorama import Fore, Style



def main():

    # init sheeps and wolf
    wolf = Wolf(config_file.wolf_move_dist)
    sheeps = []

    for i in range(config_file.sheeps_no):
        sheep = Sheep(config_file.sheep_move_dist, config_file.init_pos_limit, i+1)
        sheeps.append(sheep)

    #simulation(wolf, sheeps, config_file.rounds_no)


def simulation(wolf, sheeps, rounds):
    for i in range(rounds):
        if get_dies_count(sheeps) == config_file.sheeps_no:
            break
        print("round_no: " + str(i + 1))
        for sheep in sheeps:
            sheep.move()
        min_distance, nearest_sheep = find_nearest_sheep(wolf, sheeps)
        wolf.try_catch_sheep(nearest_sheep, min_distance)
        # json export
        json_data = create_json(sheeps, wolf, i+1)
        write_json(i+1, json_data)
        #csv export
        write_csv(i+1, get_alive_count(sheeps))
        #terminal info
        print("wolf position" + str(wolf.position) + "\nalive:" + str(get_alive_count(sheeps)) + "\ndied:" + str(get_dies_count(sheeps)) + "\n")
        if config_file.wait:
            input(Fore.GREEN+"Press enter to continue symulation")
            print(Style.RESET_ALL)

def find_nearest_sheep(wolf, sheeps):
    min_distance = config_file.init_pos_limit + 1000
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

def get_alive_count(sheeps):
    count = 0
    for sheep in sheeps:
        if sheep.alive:
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


def write_json(round_no, data, filename='pos.json'):
    path = config_file.directory + "/" + filename

    if round_no == 1:
        with open(path, 'w') as f:
            f.write(json.dumps(data, indent=5))
    else:
        with open(path, 'a') as f:
            f.write(json.dumps(data, indent=5))


def write_csv(round_no, alive_count, filename='alive.csv'):
    path = config_file.directory + "/" + filename
    if round_no == 1:
        with open(path, mode='w') as csv_file:
            fieldnames = ['round_no', 'alive']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({'round_no': round_no, 'alive': alive_count})
    else:
        with open(path, mode='a') as csv_file:
            fieldnames = ['round_no', 'alive']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writerow({'round_no': round_no, 'alive': alive_count})



if __name__ == "__main__":
    try:
        args_parser()
        logger.init_logger()
        main()
    except KeyboardInterrupt:
        print(Style.RESET_ALL)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
