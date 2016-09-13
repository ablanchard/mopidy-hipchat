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

    def command(self):
        return '/start'

    def action(self, msg):
        playlists = self.core.playlists.as_list().get()
        uri = self.find_default_playlist(playlists)
        self.core.tracklist.add(uri=uri)
        self.core.tracklist.shuffle()
        self.core.playback.play()

    def find_default_playlist(self,playlists):
        for playlist in playlists:
            if playlist.name == self.config['default_playlist']:
                return playlist.uri
