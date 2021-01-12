import json
import csv
from . import logger
from .sheep import *
from .wolf import *
from colorama import Fore, Style
from scipy.spatial import distance

class ChaseSimulation:

    def __init__(self, rounds_no, sheeps_no, init_pos_limit, sheep_move_dist, wolf_move_dist, wait, directory):
        # init config parameters validation
        try:
            self._rounds_no = int(rounds_no)
            self._sheeps_no = int(sheeps_no)
            self._init_pos_limit = float(init_pos_limit)
            self._sheep_move_dist = float(sheep_move_dist)
            self._wolf_move_dist = float(wolf_move_dist)
            self._wait = bool(wait)
            self._directory = directory

            if rounds_no < 1:
                logger.get_logger().error("Wrong rounds_no value")
                raise ValueError("Wrong rounds_no value")
            if sheeps_no < 1:
                logger.get_logger().error("Wroung sheeps_no value")
                raise ValueError("Wroung sheeps_no value")
            if sheep_move_dist <= 0:
                logger.get_logger().error("Wrong sheep_move_dist value")
                raise ValueError("Wrong sheep_move_dist value")
            if wolf_move_dist <= 0:
                logger.get_logger().error("Wrong wolf_move_dist value")
                raise ValueError("Wrong wolf_move_dist value")

                # init animals
            self.init_animals()

        except:
            logger.get_logger().error("Wrong values types")
            raise ValueError("Wrong values types")



    def init_animals(self):
        self._wolf = Wolf(self._wolf_move_dist)
        self._sheeps = []

        for i in range(self._sheeps_no):
            sheep = Sheep(self._sheep_move_dist, self._init_pos_limit, i + 1)
            self._sheeps.append(sheep)

        log = f"Animals:  wolf: {self._wolf}, sheeps: {self._sheeps}"
        logger.get_logger().debug(log)

    def simulate(self):
        for i in range(self._rounds_no):
            if self.get_dies_count() == self._sheeps_no:
                break
            round_log = f"round_no: {i + 1}"
            print(Fore.CYAN + round_log + Style.RESET_ALL)
            # json export
            if i == 0:
                json_data = self.create_json(i)
                self.write_json(i, json_data)
            for sheep in self._sheeps:
                sheep.move()
            min_distance, nearest_sheep = self.find_nearest_sheep()
            start_wolf_position = [round(pos, 3) for pos in self._wolf.get_position()]
            killed_sheep_index = self._wolf.try_catch_sheep(nearest_sheep, min_distance)
            # json export
            json_data = self.create_json(i+1)
            self.write_json(i, json_data)
            # csv export
            self.write_csv(i + 1, self.get_alive_count())

            end_wolf_position = [round(pos, 3) for pos in self._wolf.get_position()]
            other_info_log = f"wolf start position: {start_wolf_position}\nalive: {self.get_alive_count()}\ndied: {self.get_dies_count()}\nwolf end position{end_wolf_position}\n"
            # terminal info
            if killed_sheep_index is not None:
                killed_sheep_index_log = f"sheep died: {killed_sheep_index}\n"
                other_info_log += killed_sheep_index_log
                # print(Fore.RED + killed_sheep_index_log, end='')

            print(other_info_log.replace("sheep died", Fore.RED + "sheep died"))

            logger.get_logger().info(round_log + ", " + other_info_log[:-1].replace("\n", ", "))
            if self._wait:
                input(Fore.GREEN + "Press enter to continue symulation")
            print(Style.RESET_ALL)

    def find_nearest_sheep(self):
        min_distance = self._init_pos_limit + 1000
        nearest_sheep = self._sheeps[0]
        for sheep in self._sheeps:
            if sheep.alive:
                dist = distance.euclidean(self._wolf.get_position(), sheep.get_position())
                if dist < min_distance:
                    min_distance = dist
                    nearest_sheep = sheep

        log = f"min_distance: {min_distance}, nearest_sheep: {nearest_sheep}"
        logger.get_logger().debug(log)
        return min_distance, nearest_sheep

    def get_dies_count(self):
        count = 0
        for sheep in self._sheeps:
            if not sheep.alive:
                count += 1

        log = f"dies_count: {count}"
        logger.get_logger().debug(log)

        return count

    def get_alive_count(self):
        count = 0
        for sheep in self._sheeps:
            if sheep.alive:
                count += 1

        log = f"alive_count: {count}"
        logger.get_logger().debug(log)

        return count

    def create_json(self, round_no):
        x = {
            "round_no": round_no,
            "wolf_pos": {"x": self._wolf.get_x(),
                         "y": self._wolf.get_y()}
        }
        sheeps_pos = []
        for sheep in self._sheeps:
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

    def write_json(self, round_no, data, filename='pos.json'):
        path = self._directory + "/" + filename

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

    def write_csv(self, round_no, alive_count, filename='alive.csv'):
        path = self._directory + "/" + filename
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

