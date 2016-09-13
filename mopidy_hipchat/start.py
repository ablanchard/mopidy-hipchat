# stdlib imports
import json
import logging
import time

from lol import log_dict



from listener import CommandListener


logger = logging.getLogger(__name__)

class StartListener(CommandListener):

    def __init__(self,core):
        self.core = core

    def command(self):
        return '/start'

    def action(self, msg):
        pass