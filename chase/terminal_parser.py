import argparse
import configparser
import os
import logging
from . import logger, parameters


def args_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config', metavar='FILE',
                        help="config file name", action='store', dest='config_file', type=str)

    parser.add_argument('-d', '--dir', metavar='DIR', action='store',
                        help="dictionary name for saving files", dest='directory', type=str)

    parser.add_argument('-l', '--log', metavar='LEVEL', action='store',
                        help="init logging with log LEVEL :[DEBUG, INFO, WARNING, ERROR, CRITICAL]", dest='log_level', type=str)

    parser.add_argument('-r', '--rounds', metavar='NUM', action='store',
                        help="rounds number", dest='rounds_no', type=int)

    parser.add_argument('-s', '--sheep', metavar='NUM', action='store',
                        help="sheeps count", dest='sheeps_no', type=int)

    parser.add_argument('-w', '--wait', action='store_true',
                        help="wait after each round of simulation")

    args = parser.parse_args()

    if args.log_level is not None:
        error_levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }

        if args.log_level not in error_levels:
            raise ValueError("Wrong log level")
        else:
            logger.init_logger(error_levels[args.log_level])

    if args.config_file is not None:
        config = configparser.ConfigParser()
        config.read(args.config_file)

        try:
            init_limit = float(config.get('Terrain', 'InitPosLimit'))
            sheep_dist = float(config.get('Movement', 'SheepMoveDist'))
            wolf_dist = float(config.get('Movement', 'WolfMoveDist'))
        except:
            logger.get_logger().error("Wrong types in config.ini")
            raise ValueError("Wrong types in config.ini")

        if init_limit > 0:
            parameters.init_pos_limit = float(init_limit)
        else:
            logger.get_logger().error("Wrong init_limit value")
            raise ValueError("Wrong init_limit value")

        if sheep_dist > 0:
            parameters.sheep_move_dist = float(sheep_dist)
        else:
            logger.get_logger().error("Wrong sheep_distance value")
            raise ValueError("Wrong sheep_distance value")

        if wolf_dist > 0:
            parameters.wolf_move_dist = float(wolf_dist)
        else:
            logger.get_logger().error("Wrong wolf_distance value")
            raise ValueError("Wrong wolf_distance value")

    if args.directory is not None:
        parameters.directory = args.directory
        try:
            os.mkdir(parameters.directory)
        except OSError:
            logger.get_logger().error("Creation of the directory %s failed" % parameters.directory)

    if args.rounds_no is not None:
        if args.rounds_no < 0:
            logger.get_logger().error("Wrong rounds_no value")
            raise ValueError("Wrong rounds_no value")

        parameters.rounds_no = args.rounds_no

    if args.sheeps_no is not None:
        if args.sheeps_no < 0:
            logger.get_logger().error("Wrong sheeps_no value")
            raise ValueError("Wrong sheeps_no value")

        parameters.sheeps_no = args.sheeps_no

    if args.wait:
        parameters.wait = True
