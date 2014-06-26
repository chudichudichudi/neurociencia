'''
Created on Jan 6, 2012

@author: mariano
'''
from multineuro.sprite import ImgSprite
from multineuro.sprite.tipsprite import SingleTipSprite

class Slider(SingleTipSprite):
    ''' Touchable sprite, call callback on touch. '''


    def __init__(self, pos, callback=None, resource=None, image=None):

        if resource:
            sprite = ImgSprite(resource, pos)
            rect = sprite.rect
            image = sprite.image
        else:
            rect = image.get_rect()
            rect.move_ip(pos[0], pos[1])
        super(Slider, self).__init__(rect=rect, image=image)
        if callback is not None:
            self.suscribe('touch', callback)

    def tip_update(self, tip):
        self.hide()
        scale = float(tip.pos()[0] - self.rect.left)/ self.rect.w
        print scale
        #Cuentita relativo con rect
        self.dispatch("touch", scale)
