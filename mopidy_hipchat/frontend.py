# future imports
from __future__ import absolute_import
from __future__ import unicode_literals

# stdlib imports
import logging

# third-party imports
import pykka

# local imports
from .reporters import events
from . import connector
from . import lol
from . import help
from . import request
from . import next

logger = logging.getLogger(__name__)


class HipchatFrontend(pykka.ThreadingActor):

    def __init__(self, config, core):
        super(HipchatFrontend, self).__init__()
        self.config = config
        self.core = core
        self.event_reporter = None
        self.user_command_controller = None
        self.hipchat_connector =  connector.HipchatConnector(self.config['hipchat'])
        self.help_listener = help.HelpListener()
        self.request_listener = request.RequestListener(self.core)
        self.next_listener = next.NextListener(self.core)
        self.hipchat_connector.register_to_command(self.help_listener)
        self.hipchat_connector.register_to_command(self.request_listener)
        self.hipchat_connector.register_to_command(self.next_listener)

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
