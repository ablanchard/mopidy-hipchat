# stdlib imports
import json
import logging
import time

from lol import title_dash_artist



from listener import CommandListener


logger = logging.getLogger(__name__)

class RequestListener(CommandListener):

    def __init__(self,core):
        self.core = core

    def command(self):
        return '/request'

    def action(self, msg):
        query = {'any': msg['body'][8:].strip().split(' ')}
        results = self.core.library.search(query).get()
        logger.info(str(results))
        logger.info('{} results matching query {} and uri {}'.format(len(results[0].tracks), query, results[0].uri))
        if len(results[0].tracks) <= 0:
            return 'Nothing match your query :('
        else:
            current_track_position = self.core.tracklist.index().get()
            current_track_position = -1 if current_track_position is None else current_track_position
            logger.info('current position {}'.format(current_track_position))
            add = [results[0].tracks[0]]
            self.core.tracklist.add(tracks=add,
                                    at_position=current_track_position + 1)
            return '{} will be played next'.format(title_dash_artist(results[0].tracks[0]))