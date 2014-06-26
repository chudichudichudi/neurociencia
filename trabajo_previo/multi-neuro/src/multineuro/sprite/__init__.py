""" Contains Sprite classes. """
from multineuro.sprite.initializable import InitializableSprite, screen_size
from tipsprite import SingleTipSprite
import pygame
from multineuro.tips.tipsutils import scale
import sys
import os
from pygame import rect
import logging


class ImgSprite(InitializableSprite):
    """ A DirtySprite created from an image. """
    def __init__(self, img_path, pos=(0, 0)):
        super(ImgSprite, self).__init__()
        try:
            self.image = pygame.image.load(img_path)
        except pygame.error:
            logging.error('Could not load image file: %s',
                          os.path.join(os.getcwd(), img_path))
            raise IOError()
        self.rect = pygame.Rect(pos, self.image.get_size())

    def initialize_sprite(self):
        super(ImgSprite, self).initialize_sprite()
        self.image.convert_alpha()
        self.image = self.image.convert()
        self.dirty = 1



class MovableSprite(SingleTipSprite):
    """ A SingleTipSprite that allows to be moved """
    def __init__(self, sprite):
        super(MovableSprite, self).__init__(rect=sprite.rect,
                                            image=sprite.image)

    def tip_update(self, tip):
        pos = tip.pos(self.global_size)
        prev = (self.rect.left, self.rect.top)
        self.rect.left = pos[0] - self.offset[0]
        self.rect.top = pos[1] - self.offset[1]
        self.dirty = 1
        self.dispatch('position',
                      (pos[0] - prev[0],
                       pos[1] - prev[1]))

class RootTipSprite(SingleTipSprite):
    """TipSprite Root."""
    def __init__(self, root_surface, group, layers):
        """ Construct the RootTipSprite, it should gad a surface that occupies 
        the whole screen. """
        super(RootTipSprite, self).__init__(image=root_surface)
        self.initialize_sprite()
        self.root_surface = root_surface
        self.group = group
        self.layers = layers

    def handle_tip(self, tip):
        """ Transverse the sprite tree recursevely in order to handle the 
        tip. """
        self._group_handle_tip(tip)

    def tip_update(self, _):
        raise Exception('Shouldn\'t manage tips')






class ButtonSprite(SingleTipSprite):
    """ Hidden button in the corners of the screen. """

    corners = {'top-left': (0, 0),
              'top-right': (1, 0),
              'bottom-left': (0, 1),
              'bottom-right': (1, 1)
              }

    def __init__(self, corner):
        assert corner in self.corners
        super(ButtonSprite, self).__init__()
        self.corner = self.corners[corner]
        self.diameter = 128
        self.size = (self.diameter, self.diameter)
        self.image = pygame.Surface(self.size)
        self.image.fill((255, 255, 255))
        self.rect = pygame.Rect((0, 0), self.size)

    def initialize_sprite(self):
        super(ButtonSprite, self).initialize_sprite()
        self.rect.center = scale(self.corner, self.global_size)

    def tip_update(self, _):
        """ A."""
        self.dispatch('pressed', self)
        self.unsuscribe_tip()
