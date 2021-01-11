import logging

from chase.data import config_file


def init_logger(level):
    path = config_file.directory + "/" + "chase.log"
    logging.basicConfig(level=level, filename=path, filemode='w',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.info('Init logger')


def get_logger():
    return logging.getLogger(__name__)
