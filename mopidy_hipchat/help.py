# stdlib imports
import json
import logging
import time



from listener import CommandListener


logger = logging.getLogger(__name__)

class HelpListener(CommandListener):

    def command(self):
        return '/help'

    def action(self, msg):
        return '/request song_name - Request a new song to be played\n' \
                    '/help - Display this help'