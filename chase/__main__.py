import os
import sys
from colorama import Fore, Style
from . import logger
from chase.data import config_file
from chase.chase_simulation import ChaseSimulation
from chase.config import args_parser

def main():
    log = f"Game config:  rounds: {config_file.rounds_no}, sheeps_no: {config_file.sheeps_no}, " \
          f"init_pos_limit: {config_file.init_pos_limit}, sheep_move_dist: {config_file.sheep_move_dist}, " \
          f"wolf_move_dist {config_file.wolf_move_dist}"
    logger.get_logger().info(log)

    chase_simulation = ChaseSimulation(config_file.rounds_no, config_file.sheeps_no, config_file.init_pos_limit,
                                     config_file.sheep_move_dist, config_file.wolf_move_dist, config_file.wait,
                                     config_file.directory)

    chase_simulation.simulate()

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