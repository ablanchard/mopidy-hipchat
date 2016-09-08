# future imports
from __future__ import unicode_literals

# stdlib imports
import logging

# third-party imports
import sleekxmpp
import pykka


logger = logging.getLogger(__name__)

class HipchatConnector(sleekxmpp.ClientXMPP, pykka.ThreadingActor):

    def __init__(self, config):
        sleekxmpp.ClientXMPP.__init__(self, config['jid'], config['password'])
        self.room = config['room_id']
        self.nick = 'Radio'

    def start_xmpp_session(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.get_roster()
        self.send_presence()

        logger.info(self.room)
        logger.info(self.nick)

        self.plugin['xep_0045'].joinMUC(self.room,self.nick, wait=True)


    def on_start(self):
        logger.info('UserCommandController started.')
        self.add_event_handler('session_start', self.start_xmpp_session)
        self.add_event_handler('message', self.message)
        self.add_event_handler("groupchat_message", self.muc_message)

        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data Forms
        self.register_plugin('xep_0060') # PubSub
        self.register_plugin('xep_0045') # GroupChat
        self.register_plugin('xep_0199') # XMPP Ping
        if self.connect():
            self.process(block=True)
            logger.info('Connected to hipchat')

    def muc_message(self, msg):
        logger.info(msg)
        if msg['mucnick'] != self.nick and self.nick in msg['body']:
            self.send_message(mto=msg['from'].bare,
                              mbody="I heard that, %s." % msg['mucnick'],
                              mtype='groupchat')


    def message(self, msg):
        """
        Process incoming message stanzas. Be aware that this also
        includes MUC messages and error messages. It is usually
        a good idea to check the messages's type before processing
        or sending replies.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        if msg['type'] in ('chat', 'normal'):
            logger.info(msg)


    def send_notification(self, message, color, notify):
        """Sends a HTTP request to the configured server.

        All exceptions are suppressed but emit a warning message in the log.
        """
        logger.debug('will send {0}'.format(message))
        #self.room.notification(message, color, notify, 'text')

    def get_latest(self,latestId):
        return self.room.latest(latestId,10)

    
