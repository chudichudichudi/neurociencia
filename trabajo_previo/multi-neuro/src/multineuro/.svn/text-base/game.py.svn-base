from sprite import RootTipSprite
#pylint: disable=W0622
from threading import enumerate, current_thread, Timer
#pylint: enable=W0622
import pygame
from multineuro.sprite.initializable import InitializableSprite, screen_size
from multineuro.pygamedev import PygameTips
from multineuro.sprite.textsprite import TextSprite
import logging

GUI = 3
ACTIVE = 2
BACKGROUND = 1


class Game(object):
    ''' Game class, it manages input from a multitouch device, 
    and handle sprite with a layered behaviour. 
    '''
    def __init__(self, name, fullscreen=False, tuio=True, background=None):
        self._ended = False
        logging.log(logging.DEBUG, 'Initializing Tips + Mouse')
        self.tips = PygameTips(tuio)
        if not background:
            background = 255, 255, 255
        self.background_color = background
        self.name = name
        logging.log(logging.DEBUG, 'Initializing Pygame.')
        self._pygame_init()
        self.fullscreen = fullscreen
        self._form = None


    def _pygame_init(self):
        pygame.init()
        pygame.display.set_caption(self.name)
        pygame.event.set_blocked(None)
        pygame.event.set_allowed([pygame.QUIT,
                                  pygame.KEYDOWN,
                                  pygame.MOUSEMOTION,
                                  pygame.MOUSEBUTTONDOWN,
                                  pygame.MOUSEBUTTONUP])
        self.clock = pygame.time.Clock()
        self.global_size = screen_size()
        self._sprites_init()

    def _sprites_init(self):
        self.group = pygame.sprite.LayeredDirty()
        self._create_background()

    def _load_sound(self, path_to_sound):
        return pygame.mixer.Sound(path_to_sound)

    def _create_background(self):
        background_surf = pygame.Surface(self.global_size)
        background_surf.fill(self.background_color)
        self.background = InitializableSprite()
        self.background.image = background_surf
        self.background.rect = pygame.Rect((0, 0), self.global_size)
        self.background.dirty = 1
        self.add_background_sprite(self.background)

    def add_background_sprite(self, sprite):
        self.group.add(sprite , layer=BACKGROUND)

    def add_active_sprite(self, sprite):
        self.group.add(sprite , layer=ACTIVE)

    def _add_gui_sprite(self, sprite):
        self.group.add(sprite, layer=GUI)

    def close(self):
        ''' Called when the game's finished. '''
        self.tips.stop()

    def _is_finnish_event(self, event):
        quit_keys = [pygame.K_ESCAPE, pygame.K_q]
        return event.type == pygame.QUIT or event.key in quit_keys

    def _exited(self):
        events = pygame.event.get([pygame.QUIT, pygame.KEYDOWN])
        return self._ended or any([self._is_finnish_event(ev) for ev in events])

    def game_over(self):
        ''' Call to end the game '''
        self._ended = True

    def show_message(self, message, time=None, callback=None):
        """ Shows a message in the screen, if time (seconds) is provided, it
            will show only for the given time. """
        text = TextSprite(message, callback)
        text.show()
        self._add_gui_sprite(text)
        if time:
            timer = Timer(time, text.hide)
            timer.start()

    def registerForm(self, form, callback):
        self._form = form
        self._form_callback = callback


    def frame(self):
        ''' Should override, it's called once per frame '''
        pass

    def _handle_new_tip(self, tip):
        self.window.handle_tip(tip)

    def _init_window(self):
        if self.fullscreen:
            options = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
            window = pygame.display.set_mode((0, 0), options)
        else:
            window = pygame.display.set_mode((1024, 768))
        self.window = RootTipSprite(window, self.group, [3, 2])
        self._initialize_sprites()
        if self._form is not None:
            self._form_callback(self._form.run(window))


    def _initialize_sprites(self):
        for sprite in self.group.sprites():
            sprite.initialize_sprite()


    def start(self):
        ''' starts the game'''
        logging.log(logging.DEBUG, 'Initializing Window.')
        self._init_window()
        logging.debug('Post-Initializing Tips')
        self.tips.initialize()
        try:
            while 1:
                #Now using DirtySprites, should only blit those which change.
                self.group.draw(self.window.image)

                #User defined
                self.frame()


                #Refresh Display
                pygame.display.flip()
                self.clock.tick(60)

                #Receive pressings
                for tip in self.tips.new_tips():
                    self._handle_new_tip(tip)

                #Finnish
                if self._exited():
                    self.close()
                    return
        except KeyboardInterrupt :
            return

    @staticmethod
    def kill():
        for thread in enumerate():
            if thread.ident != current_thread().ident:
                if 'multi' in thread.name:
                    thread.finnish()
                else:
                    logging.debug(str(thread.name) + ' is Alive')
        pygame.quit()
