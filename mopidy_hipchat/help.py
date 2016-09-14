# stdlib imports
import json
import logging
import time



from listener import CommandListener


logger = logging.getLogger(__name__)

class HelpListener(CommandListener):

    def __init__(self, hipchat_connector):
        self.hipchat_connector = hipchat_connector

    def command(self):
        return '/help'

    def action(self, msg):
        usage =''
        for listener in self.hipchat_connector.listeners:
            usage += listener.usage() + '\n'
        return usage

    def usage(self):
        return '/help - Display this help'