# stdlib imports
import json
import logging
import time

from lol import title_dash_artist



from listener import CommandListener


logger = logging.getLogger(__name__)

class RequestListener(CommandListener):

    def __init__(self,core,config):
        self.core = core
        self.config = config

    def command(self):
        return '/request'

    def action(self, msg):
        query = {'any': msg['body'][8:].strip().split(' ')}
        results = self.core.library.search(query).get()
        logger.info(str(results))
        source = self.find_best_source(results)
        logger.info('{} results matching query {} and uri {}'.format(len(source.tracks), query, source.uri))
        if len(source.tracks) <= 0:
            return 'Nothing match your query :('
        else:
            current_track_position = self.core.tracklist.index().get()
            current_track_position = -1 if current_track_position is None else current_track_position
            logger.info('current position {}'.format(current_track_position))
            add = [source.tracks[0]]
            self.core.tracklist.add(tracks=add,
                                    at_position=current_track_position + 1)
            return 'Coming next {}'.format(title_dash_artist(source.tracks[0]))

    def usage(self):
        return '/request song_name - Request a new song to be played'

    def find_best_source(self,sources):
        sources_by_uri = {}
        for source in sources:
            sources_by_uri[source.uri] = source

        sources_order = self.config['backend_priority'].split(',')
        for order in sources_order:
            if len(sources_by_uri[order + ':search'].tracks) > 0:
                return sources_by_uri[order + ':search']

        return None
