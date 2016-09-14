# stdlib imports
import json
import logging
import time

from mopidy.core import CoreListener

from lol import log_dict
from threading import Timer


from listener import CommandListener


logger = logging.getLogger(__name__)

class KeepListener(CommandListener):

    def __init__(self,core,counter):
        self.core = core
        self.counter = counter

    def command(self):
        return '/keep'

    def action(self, msg):
        self.counter.add_keep(msg['mucnick'])
        return 'Currently {} nexts and {} keeps'.format(len(self.counter.nexts),len(self.counter.keeps))
