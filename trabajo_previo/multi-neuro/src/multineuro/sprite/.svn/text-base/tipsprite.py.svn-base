''' 
    Sprites and Groups prepared to handle Tips.
'''
from multineuro.event import Event
from multineuro.sprite.initializable import InitializableSprite

DEFAULT_LAYER = 2 #ACTIVE layer in game.py

class SingleTipSprite(InitializableSprite, Event):

    """Sprite to handle a single tip"""

    def __init__(self, tip=None, image=None, rect=None):
        super(SingleTipSprite, self).__init__()
        Event.__init__(self)
        self.rect = rect
        self.image = image
        self.layers = []
        self.group = None
        self.suscription = None
        self.suscriptable = True
        if tip:
            self.handle_tip(tip)

    def _tip_update(self, tip):
        if self.visible == 1:
            self.tip_update(tip)

    def tip_update(self, _):
        '''
        Method called each time this Sprite is pressed o a tip that pressed
        this Sprite is moved.
        @param tip: The current tip
        @type tip: Tip
        '''
        raise Exception('Abstract, must implement')


    def handle_tip(self, tip):
        if self.visible and self.rect.collidepoint(tip.pos(self.global_size)):
            return self._bind_tip(tip)
        else:
            return self._group_handle_tip(tip)

    def busy(self):
        '''
        Returns True if this Sprite is pressed or moving.
        '''
        return self.suscription is not None

    def _bind_tip(self, tip):
        """ ***Single Tip*** (for a multitip this should handle a list/set) """
        return self.suscriptable and self._do_bind_tip(tip)

    def _do_bind_tip(self, tip):
        self.unsuscribe_tip()
        self.suscription = tip.suscribe('update', self._tip_update)
        tip.suscribe('finnish', lambda _: self.unsuscribe_tip())
        pos = tip.pos(self.global_size)
        self.offset = (pos[0] - self.rect.left, pos[1] - self.rect.top)
        self._tip_update(tip)
        return True


    def unsuscribe_tip(self):
        ''' Unsuscribe tip from current tip. '''
        if self.suscription is not None:
            self.suscription.unsuscribe()
            self.suscription = None

    def _group_handle_tip(self, tip):
        """ iterate over groups in order of importance (higher to lower) """
        for layer in self.layers:
            for sprite in self.group.get_sprites_from_layer(layer):
                try:
                    if sprite.handle_tip(tip):
                        return True
                except AttributeError:
                    pass
        return False


    def start_to_listen(self):
        self.suscriptable = True

    def stop_listening(self):
        self.suscriptable = False

    def hide(self):
        InitializableSprite.hide(self)
        self.unsuscribe_tip()
        self.stop_listening()

    def show(self):
        InitializableSprite.show(self)
        self.start_to_listen()



