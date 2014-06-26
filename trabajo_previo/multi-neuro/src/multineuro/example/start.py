'''
Created on Jan 11, 2012

@author: mariano
'''
from multineuro.game import Game
from multineuro.sprite.tipsprite import SingleTipSprite
from pygame import Surface
import pygame
from multineuro.sprite import ImgSprite
from multineuro.forms.forms import Form
from multineuro.forms.input import Input

class Start(Game):


    def __init__(self, name):
        super(Start, self).__init__(name)
        form = Form(True)
        form.add_object('Name', Input('Nombre', '',
                                label_size=18,
                                input_border_color=(255, 100, 100),
                                input_border_width=0,
                                input_bg_color=(0, 0, 0, 0)))
        self.registerForm(form, self.process_answer)
        self.add_background_sprite(ImgSprite('/home/mariano/proyectos/mariano-semelman/multi-game/multi-neuro/media/test.png', (100, 100)))
        self.add_active_sprite(SimpleSprite(self.show_message))

    def process_answer(self, answers):
        print answers['Name']

class SimpleSprite(SingleTipSprite):

    def __init__(self, callback):
        self.callback = callback
        super(SimpleSprite, self).__init__()
        self.image = Surface((100, 100))
        self.image.fill((240, 240, 240))
        pygame.draw.circle(self.image, (0, 0, 0), (50, 50), 50)
        self.rect = pygame.Rect((500, 500), (100, 100))

    def tip_update(self, tip):
        click_position = str(tip.pos(self.global_size))
        self.callback("LLego por: " + click_position)


def main():
    exp = None
    error = False
    try:
        #Should extend Game!
        exp = Start('Example')
        exp.start()
    except Exception:
        error = True
        raise
    finally:
        if error and exp:
            exp.close()

if __name__ == '__main__':
    main()
