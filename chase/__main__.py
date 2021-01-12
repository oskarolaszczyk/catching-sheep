import os
import sys
from colorama import Style
from . import logger, parameters
from .chase_simulation import ChaseSimulation
from .terminal_parser import args_parser

def main():
    log = f"Game config:  rounds: {parameters.rounds_no}, sheeps_no: {parameters.sheeps_no}, " \
          f"init_pos_limit: {parameters.init_pos_limit}, sheep_move_dist: {parameters.sheep_move_dist}, " \
          f"wolf_move_dist {parameters.wolf_move_dist}"
    logger.get_logger().info(log)

    chase_simulation = ChaseSimulation(parameters.rounds_no, parameters.sheeps_no, parameters.init_pos_limit,
                                       parameters.sheep_move_dist, parameters.wolf_move_dist, parameters.wait,
                                       parameters.directory)

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