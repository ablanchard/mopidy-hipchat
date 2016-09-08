# future imports
from __future__ import unicode_literals

# stdlib imports
import json
import logging

# third-party imports
import requests
from mopidy.models import ModelJSONEncoder

from hypchat import *


logger = logging.getLogger(__name__)

class HipchatConnector:

    def __init__(self, config):
        self.hc = HypChat(config['hipchat_auth_token'], endpoint=config['hipchat_domain'])
        self.room = self.hc.get_room(config['room_id'])


    def send_notification(self, message, color, notify):
        """Sends a HTTP request to the configured server.

        All exceptions are suppressed but emit a warning message in the log.
        """
        logger.debug('will send {0}'.format(message))
        self.room.notification(message, color, notify, 'text')

    def get_latest(self,latestId):
        return self.room.latest(latestId,10)

    
