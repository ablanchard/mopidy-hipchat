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
        uri = self.find_default_playlist(playlists)
        self.core.tracklist.add(uri=uri)
        self.core.tracklist.shuffle()
        self.core.playback.play()
        self.started = True
        return 'On air'

    def usage(self):
        return '/start - Start the radio broadcast'

    def find_default_playlist(self,playlists):
        for playlist in playlists:
            if playlist.name == self.config['default_playlist']:
                return playlist.uri
