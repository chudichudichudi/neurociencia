#!/usr/bin/python
'''
Created on Jan 11, 2012

@author: mariano
'''
from multineuro.game import Game
from multineuro.sprite import ImgSprite
from multineuro.sprite.textsprite import TextSprite

class Start(Game):


    def __init__(self, name):
        super(Start, self).__init__(name)
        self.add_background_sprite(ImgSprite('/home/mariano/proyectos/mariano-semelman/multi-game/multi-neuro/media/test.png', (100, 100)))
        self.text = FPSText()
        self.add_active_sprite(self.text)

    def _frame(self):
        self.text.value(self.clock.get_fps())

class FPSText(TextSprite):

    def __init__(self):
        super(FPSText, self).__init__('0.0')

    def value(self, fps):
        self.update_message(str(fps))

    def tip_update(self, tip):
        pass


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
