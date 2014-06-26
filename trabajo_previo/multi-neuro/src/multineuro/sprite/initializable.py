'''
Created on Nov 28, 2011

@author: mariano
'''
from pygame.sprite import DirtySprite
from pygame import transform, display

class InitializableSprite(DirtySprite):
    '''
    A Sprite that has a initilization method after creation.
    '''

    def __init__(self, *groups):
        super(InitializableSprite, self).__init__(*groups)
        self.full_size = False
        self._center = False

    def initialize_sprite(self):
        self.global_size = screen_size()
        if self.full_size:
            self.image = transform.scale(self.image, self.global_size)
            self.rect = self.image.get_rect()
        if self._center:
            self.rect = self.image.get_rect()
            self.rect.center = (self.global_size[0] / 2,
                                self.global_size[1] / 2)

    def set_full_size(self):
        self.full_size = True

    def center(self):
        self._center = True

    def show(self):
        self.visible = 1
        self.dirty = 1

    def hide(self):
        self.visible = 0
        self.dirty = 1

def screen_size():
    '''  '''
    assert display.get_init()
    info = display.Info()
    return (info.current_w, info.current_h)
