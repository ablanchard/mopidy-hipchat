import logging


logger = logging.getLogger(__name__)

def log_dict(dict):
    for x in dict:
        logger.info (str(x) + ':' + str(dict[x]))

def title_dash_artist(track):
    return track.name + " - " + iter(track.artists).next().name