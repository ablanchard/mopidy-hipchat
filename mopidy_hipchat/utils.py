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


def send_webhook(config, message, color, notify):
    """Sends a HTTP request to the configured server.

    All exceptions are suppressed but emit a warning message in the log.
    """
    logger.debug('will send {0}'.format(message))
    hc = HypChat(config['hipchat_auth_token'], endpoint=config['hipchat_domain'])
    room = hc.get_room(config['room_id'])
    room.notification(message, color, notify, 'text')
