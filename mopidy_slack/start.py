# stdlib imports
import json
import logging
import time

from . import listener


logger = logging.getLogger(__name__)

class StartListener(listener.CommandListener):

    def __init__(self,core, config):
        self.core = core
        self.config = config
        self.started = False

    def command(self):
        return 'start'

    def action(self, msg, user):
        if self.started:
            return 'Already started'

        playlists = self.core.playlists.as_list().get()
        query = self.config['default_playlist'] if msg[7:] == "" else msg[7:]
        uri = self.find_playlist(playlists, query)
        self.core.tracklist.add(uris=[uri])
        self.core.tracklist.shuffle()
        self.core.playback.play()
        self.started = True
        return 'On air'

    def usage(self):
        return 'start - Start the radio broadcast'

    def find_playlist(self, playlists, query):
        for playlist in playlists:
            if playlist is not None and playlist.name.lower().startswith(query.lower()):
                return playlist.uri
        return "spotify:playlist:2TYKzbVRYsyaVsPrnn2AnY"
