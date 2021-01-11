import argparse
import logging
import configparser
import os
import logging
import logger
from data import config_file


def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help="set config file", action='store', dest='config_file', metavar='FILE')
    parser.add_argument('-d', '--dir', action='store', help="choose where to save files", dest='directory',
                        metavar='DIR')
    parser.add_argument('-l', '--log', action='store', help="create log file with log LEVEL", dest='log_lvl',
                        metavar='LEVEL')
    parser.add_argument('-r', '--rounds', action='store',
                        help="choose for how many rounds should the simulation run", dest='rounds_no',
                        type=int, metavar='NUM')
    parser.add_argument('-s', '--sheep', action='store',
                        help="choose how many sheep in the simulation", dest='sheeps_no', type=int,
                        metavar='NUM')
    parser.add_argument('-w', '--wait', action='store_true', help="wait for input after each round")

    args = parser.parse_args()

    if args.config_file is not None:
        config = configparser.ConfigParser()
        config.read(args.config_file)
        init_limit = float(config.get('Terrain', 'InitPosLimit'))
        sheep_dist = float(config.get('Movement', 'SheepMoveDist'))
        wolf_dist = float(config.get('Movement', 'WolfMoveDist'))

        if init_limit > 0:
            config_file.init_pos_limit = init_limit
        else:
            raise ValueError("Not positive number")

        if sheep_dist > 0:
            config_file.sheep_move_dist = sheep_dist
        else:
            raise ValueError("Not positive number")

        if wolf_dist > 0:
            config_file.wolf_move_dist = wolf_dist
        else:
            raise ValueError("Not positive number")

    if args.directory is not None:
        config_file.directory = args.directory
        try:
            os.mkdir(config_file.directory)
        except OSError:
            print("Creation of the directory %s failed" % config_file.directory)

    if args.log_lvl is not None:
        error_levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }

        if args.log_lvl not in error_levels:
            raise ValueError("Invalid log level!")
        else:
            logger.init_logger(error_levels[args.log_lvl])

    if args.rounds_no is not None:
        if args.rounds_no < 0:
            raise ValueError("Value must be positive")

        config_file.rounds_no = args.rounds_no

    if args.sheeps_no is not None:
        if args.sheeps_no < 0:
            raise ValueError("Value must be positive")
        config_file.sheeps_no = args.sheeps_no


    if args.wait:
        config_file.wait = True
