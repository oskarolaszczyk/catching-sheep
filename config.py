import argparse
import logging
import configparser
from data import config_file


def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help="set config file", action='store', dest='conf_file', metavar='FILE')
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
    # if args.conf_file is not None:

    # if args.directory is not None:
    #     directory = args.directory
    # if args.log_lvl is not None:
    #     if args.log_lvl == "DEBUG":
    #         lvl = logging.DEBUG
    #     elif args.log_lvl == "INFO":
    #         lvl = logging.INFO
    #     elif args.log_lvl == "WARNING":
    #         lvl = logging.WARNING
    #     elif args.log_lvl == "ERROR":
    #         lvl = logging.ERROR
    #     elif args.log_lvl == "CRITICAL":
    #         lvl = logging.CRITICAL
    #     else:
    #         raise ValueError("Invalid log level!")
    #     logging.basicConfig(level=lvl, filename="chase.log")
    #     logging.debug("debug")
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
