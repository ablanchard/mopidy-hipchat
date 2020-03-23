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
from . import keep
from . import start

logger = logging.getLogger(__name__)


class SlackFrontend(pykka.ThreadingActor):

    def __init__(self, config, core):
        super(SlackFrontend, self).__init__()
        self.config = config
        self.core = core
        self.event_reporter = None
        self.user_command_controller = None
        self.slack_connector =  connector.SlackConnector(self.config['slack'])
        self.help_listener = help.HelpListener(self.slack_connector)
        self.request_listener = request.RequestListener(self.core, self.config['slack'])
        self.next_counter = next.NextCounter()
        self.next_listener = next.NextListener(self.core,self.next_counter)
        self.keep_listener = keep.KeepListener(self.core,self.next_counter)
        self.start_listener = start.StartListener(self.core, self.config['slack'])
        self.slack_connector.register_to_command(self.help_listener)
        self.slack_connector.register_to_command(self.request_listener)
        self.slack_connector.register_to_command(self.next_listener)
        self.slack_connector.register_to_command(self.keep_listener)
        self.slack_connector.register_to_command(self.start_listener)

    def on_start(self):
        self.slack_connector.on_start()
        self.event_reporter = events.EventReporter.start(self.config, self.slack_connector, self.next_counter)

    def _stop_children(self):
        self.event_reporter.stop()
        self.slack_connector.on_stop()

    def on_stop(self):
        logger.info('Stopping slack frontend')
        self._stop_children()

    def on_failure(self, exception_type, exception_value, traceback):
        logger.info('Failure on frontend')
        self._stop_children()
