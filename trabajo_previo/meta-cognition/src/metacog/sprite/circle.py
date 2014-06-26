'''
Created on Jan 6, 2012

@author: mariano
'''

import pygame
from multineuro.sprite.tipsprite import SingleTipSprite
from multineuro.pygamedev.aacircle import AACircle
import logging

class Circle(SingleTipSprite):
    """ Handle a resizeable Circle Sprite. """

    available_circles = {}


    def __init__(self, screen_pos, position_num, max_size, *args, **kwargs):
        rect_dimension = self.get_rect_size(max_size)
        kwargs['rect'] = pygame.Rect(screen_pos, rect_dimension)
        kwargs['image'] = pygame.Surface(rect_dimension, pygame.SRCALPHA, 32)
        SingleTipSprite.__init__(self, *args, **kwargs)
        self.size = None
        self.position = position_num

    def get_rect_size(self, max_size):
        self.max_size = max_size
        rect_size = self.max_size * 2
        rect_dimension = rect_size, rect_size
        return rect_dimension

    def tip_update(self, _):
        self.dispatch('touch', self)
        self.unsuscribe_tip()

    def is_correct(self):
        return self.size == self.max_size

    def change_size(self, new_size):
        """ Effectively change sprite size. """
        if not Circle.available_circles.has_key(new_size - 1):
            logging.debug('Circle Cache miss: ' + str(new_size))
            Circle.available_circles[new_size - 1] = AACircle(new_size, color=(0, 0, 0), antialias=2)
        self.image = Circle.available_circles[new_size - 1]
        self.size = new_size
