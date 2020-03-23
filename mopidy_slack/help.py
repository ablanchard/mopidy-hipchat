# stdlib imports
import json
import logging
import time

from . import listener


logger = logging.getLogger(__name__)

class HelpListener(listener.CommandListener):

    def __init__(self, listeners):
        self.listeners = listeners

    def command(self):
        return 'help'

    def action(self, msg, user):
        usage =''
        for listener in self.listeners:
            usage += listener.usage() + '\n'
        return usage

    def usage(self):
        return 'help - Display this help'