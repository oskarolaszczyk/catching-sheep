import logging

from data import config_file

def init_logger():
    path = config_file.directory + "/" + "logs.log"
    logging.basicConfig(filename=path, filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.warning('This will get logged to a file')