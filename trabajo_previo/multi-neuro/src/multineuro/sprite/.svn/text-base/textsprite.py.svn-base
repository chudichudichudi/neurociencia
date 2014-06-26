from multineuro.sprite.tipsprite import SingleTipSprite
from pygame import rect
import pygame


class TextSprite(SingleTipSprite):
    """ Sprite used to show text in screen. """
    def update_message(self, message):
        self.image = self._create_text_surface(message)
        self.dirty = 1

    def __init__(self, message, callback=None):
        self.update_message(message)
        super(TextSprite, self).__init__(image=self.image,
                                         rect=self.image.get_rect())
        self.initialize_sprite()
        self.callback = callback
        self.rect = rect.Rect((0, 0), self.global_size)

    def tip_update(self, _):
        """ Close when clicked. """
        self.hide()
        if self.callback:
            self.callback()

    def _create_text_surface(self, message):
        font_size = 36
        background_color = 255, 255, 255
        font_color = 10, 10, 10
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(message, 1, font_color, background_color)
        return text_surface

