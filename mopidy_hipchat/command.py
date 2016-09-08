# stdlib imports
import json
import logging
import time


# third-party imports
import pykka

from utils import HipchatConnector


logger = logging.getLogger(__name__)

class UserCommandController(pykka.ThreadingActor):

    def __init__(self, config):
        super(UserCommandController, self).__init__()
        self.config = config['hipchat']
        self.hipchatConnector = HipchatConnector(self.config)
        self.HELP = '/request song_name - Request a new song to be played\n' \
                    '/help - Display this help'


    def on_start(self):
        logger.info('UserCommandController started.')
        self.monitor_messages()

    def monitor_messages(self):
        latest = ''
        while True:
            messages = self.hipchatConnector.get_latest(latest)
            for message in messages['items']:
                logger.debug('received {0}'.format(message['message']))
                if message['id'] != latest:
                    self.message_action(message['message'])
                latest = message['id']
            time.sleep(1)


    def message_action(self,message):
        split = message.split(' ')
        if split[0] == '/help':
            self.print_help()
        if split[0] == '/request':
            self.request_song(message)


    def print_help(self):
        self.hipchatConnector.send_notification(self.HELP, 'green', False)

    def request_song(self, message):
        self.hipchatConnector.send_notification('Not implemented yet :(', 'red', False)










