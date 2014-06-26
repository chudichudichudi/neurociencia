'''
Created on Apr 4, 2012

@author: mariano
'''
from multineuro.event import Event
from multineuro.tips import tipsutils
import time

EXPIRATION = 5.0

class Tip(Event):

    def __init__(self, cursor):
        super(Tip, self).__init__()
        self.cursor = cursor
        self.ident = self.cursor.sessionid
        self.last_update = time.time()

    def pos(self, scale=(1, 1)):
        return tipsutils.scale((self.cursor.xpos, self.cursor.ypos), scale)

    def update(self):
        self.last_update = time.time()
        self.dispatch('update', self)

    def mot(self, scale=(1, 1)):
        return tipsutils.scale((self.cursor.xmot, self.cursor.ymot), scale)


    def expired(self):
        return time.time() - self.last_update > EXPIRATION

    def delete(self):
        self.dispatch('finnish', self)
