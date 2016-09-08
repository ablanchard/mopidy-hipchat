# future imports
from __future__ import absolute_import
from __future__ import unicode_literals

# stdlib imports
import logging

# third-party imports
import pykka
from mopidy.core import CoreListener

# local imports
from ..utils import HipchatConnector


logger = logging.getLogger(__name__)


class EventReporter(pykka.ThreadingActor, CoreListener):

    def __init__(self, config):
        super(EventReporter, self).__init__()
        self.config = config['hipchat']
        self.hipchatConnector = HipchatConnector(self.config)

    def on_start(self):
        logger.info('EventReporter started.')

        self.hipchatConnector.send_notification('On air','red',True)
        #monitor_messages(self.config);

    def track_playback_started(self, tl_track):
        logger.info('Track started {0}'.format(tl_track))

        current_track = tl_track.track
        current_track = "None" if current_track is None else current_track.name + " - " + iter(current_track.artists).next().name
        self.hipchatConnector.send_notification(current_track, 'green', False)
