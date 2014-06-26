'''
Created on Jan 11, 2012

@author: mariano
'''
from multineuro.tips.threads import Looper, wait_free_acquire
import time
from multineuro.tips.tip import Tip
import pygame

UPDATE_PER_SECOND_POINTS = 30
MOUSE_ID = -1

class Points(Looper):
    '''
    Class that creates and updates tips that represents a click
    '''


    def __init__(self, new_tips, tips, lock):
        '''
        Constructor
        '''
        super(Points, self).__init__()
        self.new_tips = new_tips
        self.tips = tips
        self.lock = lock
        self.pressed = False
        self.pos = (0, 0)

    def main(self):
        self.analyze_mouse()
        if self.pressed:
            self._store()
        else:
            self._delete()
        time.sleep(1.0 / UPDATE_PER_SECOND_POINTS)

    def _delete(self):
        wait_free_acquire(self.lock)
        if MOUSE_ID in self.tips:
            self.tips[MOUSE_ID].delete()
            del self.tips[MOUSE_ID]
            if MOUSE_ID in self.new_tips:
                self.new_tips.remove(MOUSE_ID)
        self.lock.release()

    def analyze_mouse(self):
        for ev in pygame.event.get([pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]):
            if self.is_pressed(ev):
                self.pressed = True
                self.pos = ev.pos
            else:
                self.pressed = False

    def is_pressed(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.MOUSEMOTION and event.buttons[0])

    def _store(self):
        wait_free_acquire(self.lock)
        if MOUSE_ID in self.tips:
            self.tips[MOUSE_ID].update(self.pos)
        else:
            self.tips[MOUSE_ID] = MouseTip(self.pos)
            self.new_tips.add(MOUSE_ID)
        self.lock.release()

class MouseTip(Tip):
    # pylint: disable=W0221

    def __init__(self, pos):
        super(MouseTip, self).__init__(MouseCursorWrapper(pos))

    def expired(self):
        return False

    def update(self, pos):
        self.cursor.xpos = pos[0]
        self.cursor.ypos = pos[1]
        super(MouseTip, self).update()

    def pos(self, scale=(1, 1)): #@UnusedVariable
        return super(MouseTip, self).pos()

    def mot(self, scale=(1, 1)):
        raise Exception()

class MouseCursorWrapper(object):

    def __init__(self, pos):
        self.xpos = pos[0]
        self.ypos = pos[1]
        self.sessionid = MOUSE_ID
        self.xmot = 0
        self.ymot = 0
