'''
Created on Jan 6, 2012

@author: mariano
'''
from multineuro.sprite import ImgSprite
from multineuro.sprite.tipsprite import SingleTipSprite

class Button(SingleTipSprite):
    ''' Touchable sprite, call callback on touch. '''


    def __init__(self, pos, callback=None, resource=None, image=None, val=None,):

        if resource:
            sprite = ImgSprite(resource, pos)
            rect = sprite.rect
            image = sprite.image
        else:
            rect = image.get_rect()
            rect.move_ip(pos[0], pos[1])
        super(Button, self).__init__(rect=rect, image=image)
        self.val = val
        if callback is not None:
            self.suscribe('touch', callback)

    def tip_update(self, _):
        self.hide()
        self.dispatch("touch", self.val)





