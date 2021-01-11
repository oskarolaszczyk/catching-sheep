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
    log = f"Game config:  rounds: {config_file.rounds_no}, sheeps_no: {config_file.sheeps_no}, " \
          f"init_pos_limit: {config_file.init_pos_limit}, sheep_move_dist: {config_file.sheep_move_dist}, " \
          f"wolf_move_dist {config_file.wolf_move_dist}"
    logger.get_logger().info(log)

    wolf, sheeps = init_animals()
    simulation(wolf, sheeps, config_file.rounds_no)


# ----------OTHER FUNCTIONS----------- #


def init_animals():
    wolf = Wolf(config_file.wolf_move_dist)
    sheeps = []

    for i in range(config_file.sheeps_no):
        sheep = Sheep(config_file.sheep_move_dist, config_file.init_pos_limit, i + 1)
        sheeps.append(sheep)

    log = f"Animals:  wolf: {wolf}, sheeps: {sheeps}"
    logger.get_logger().debug(log)

    return wolf, sheeps


def simulation(wolf, sheeps, rounds):
    for i in range(rounds):
        if get_dies_count(sheeps) == config_file.sheeps_no:
            break
        round_log = f"round_no: {i+1}"
        print(Fore.CYAN + round_log + Style.RESET_ALL)
        # json export
        json_data = create_json(sheeps, wolf, i)
        write_json(i, json_data)
        for sheep in sheeps:
            sheep.move()
        min_distance, nearest_sheep = find_nearest_sheep(wolf, sheeps)
        start_wolf_position = [round(pos, 3) for pos in wolf.position]
        killed_sheep_index = wolf.try_catch_sheep(nearest_sheep, min_distance)
        # csv export
        write_csv(i + 1, get_alive_count(sheeps))

        end_wolf_position = [round(pos, 3) for pos in wolf.position]
        other_info_log = f"wolf start position: {start_wolf_position}\nalive: {get_alive_count(sheeps)}\ndied: {get_dies_count(sheeps)}\nwolf end position{end_wolf_position}\n"
        # terminal info
        if killed_sheep_index is not None:
            killed_sheep_index_log = f"sheep died: {killed_sheep_index}\n"
            other_info_log += killed_sheep_index_log
            # print(Fore.RED + killed_sheep_index_log, end='')

        print(other_info_log.replace("sheep died", Fore.RED + "sheep died"))

        logger.get_logger().info(round_log + ", " + other_info_log[:-1].replace("\n", ", "))
        if config_file.wait:
            input(Fore.GREEN + "Press enter to continue symulation")
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

    log = f"min_distance: {min_distance}, nearest_sheep: {nearest_sheep}"
    logger.get_logger().debug(log)
    return min_distance, nearest_sheep


def get_dies_count(sheeps):
    count = 0
    for sheep in sheeps:
        if not sheep.alive:
            count += 1

    log = f"dies_count: {count}"
    logger.get_logger().debug(log)

    return count


def get_alive_count(sheeps):
    count = 0
    for sheep in sheeps:
        if sheep.alive:
            count += 1

    log = f"alive_count: {count}"
    logger.get_logger().debug(log)

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

    log = f"created_json: {x}"
    logger.get_logger().debug(log)

    return x


def write_json(round_no, data, filename='pos.json'):
    path = config_file.directory + "/" + filename

    if round_no == 0:
        with open(path, 'w') as f:
            f.write(json.dumps(data, indent=5))

        log = f"json created"
        logger.get_logger().debug(log)
    else:
        with open(path, 'a') as f:
            f.write(json.dumps(data, indent=5))

        log = f"json updated"
        logger.get_logger().debug(log)


def write_csv(round_no, alive_count, filename='alive.csv'):
    path = config_file.directory + "/" + filename
    if round_no == 1:
        with open(path, mode='w') as csv_file:
            fieldnames = ['round_no', 'alive']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({'round_no': round_no, 'alive': alive_count})

        log = f"csv created"
        logger.get_logger().debug(log)
    else:
        with open(path, mode='a') as csv_file:
            fieldnames = ['round_no', 'alive']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writerow({'round_no': round_no, 'alive': alive_count})

        log = f"csv updated"
        logger.get_logger().debug(log)


if __name__ == "__main__":
    try:
        args_parser()
        main()
    except KeyboardInterrupt:
        print(Style.RESET_ALL)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
