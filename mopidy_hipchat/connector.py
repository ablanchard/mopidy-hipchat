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
        self.nick = 'Jarvis'
        self.listeners = [];

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

        self.plugin['xep_0045'].joinMUC(self.room,self.nick,maxhistory="1", wait=True)

        logger.info(self.room)
        logger.info(self.nick)

    def end_xmpp_session(self, event):
        logger.info('disconnected')



    def on_start(self):
        logger.info('UserCommandController started.')

        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data Forms
        self.register_plugin('xep_0060') # PubSub
        self.register_plugin('xep_0045') # GroupChat
        self.register_plugin('xep_0199') # XMPP Ping

        self.add_event_handler('session_start', self.start_xmpp_session)
        self.add_event_handler('session_end', self.end_xmpp_session)
        self.add_event_handler('message', self.message)
        self.add_event_handler("groupchat_message", self.muc_message)
        if self.connect():
            self.process(block=False)
            logger.info('Connected to hipchat')

    def on_stop(self):
        logger.info('Stopping hipchat connector')
        self.disconnect()

    def muc_message(self, msg):
        logger.info(msg)
        if msg['mucnick'] != self.nick:
            for listener in self.listeners:
                if msg['body'].startswith(listener.command()):
                    self.send_message(mto=msg['from'].bare,
                                      mbody=listener.action(msg),
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


    def send_notification(self, message):
        """Sends a HTTP request to the configured server.

        All exceptions are suppressed but emit a warning message in the log.
        """
        logger.debug('will send {0}'.format(message))
        self.send_message(mto=self.room,
                          mbody=message,
                          mtype='groupchat')

    def get_latest(self,latestId):
        return self.room.latest(latestId,10)

    def register_to_command(self, listener):
        self.listeners.append(listener)

    
