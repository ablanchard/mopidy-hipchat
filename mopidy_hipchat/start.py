# stdlib imports
import json
import logging
import time

from lol import log_dict



from listener import CommandListener


logger = logging.getLogger(__name__)

class StartListener(CommandListener):

    def __init__(self,core, config):
        self.core = core
        self.config =config
        self.started = False

    def command(self):
        return '/start'

    def action(self, msg):
        if self.started:
            return 'Already started'

        playlists = self.core.playlists.as_list().get()
        query = self.config['default_playlist'] if msg['body'][7:] == "" else msg['body'][7:]
        uri = self.find_playlist(playlists, query)
        self.core.tracklist.add(uri=uri)
        self.core.tracklist.shuffle()
        self.core.playback.play()
        self.started = True
        return 'On air'

    def usage(self):
        return '/start - Start the radio broadcast'

    def find_playlist(self, playlists, query):
        for playlist in playlists:
            if playlist.name == query:
                return playlist.uri
