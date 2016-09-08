# future imports
from __future__ import absolute_import
from __future__ import unicode_literals

# stdlib imports
import logging

# third-party imports
import pykka

# local imports
from .reporters import events
from . import utils
from . import lol

logger = logging.getLogger(__name__)


class HipchatFrontend(pykka.ThreadingActor):

    def __init__(self, config, core):
        super(HipchatFrontend, self).__init__()
        self.config = config
        self.core = core
        self.event_reporter = None
        self.user_command_controller = None
        self.hipchat_connector =  utils.HipchatConnector(self.config['hipchat'])

    def on_start(self):
        self.hipchat_connector.on_start()
        self.event_reporter = events.EventReporter.start(self.config, self.hipchat_connector)

    def _stop_children(self):
        self.event_reporter.stop()
        self.hipchat_connector.stop()

    def on_stop(self):
        self._stop_children()

    def on_failure(self, exception_type, exception_value, traceback):
        self._stop_children()
