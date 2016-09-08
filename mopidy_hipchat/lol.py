import logging


logger = logging.getLogger(__name__)

def log_dict(dict):
    for x in dict:
        logger.info (x)
        for y in dict[x]:
            logger.info (str(y) + ':' + str(dict[x][y]))