from multineuro.forms.text import Text
from multineuro.forms.text_input import TextInput
import pygame
from multineuro.forms.form_object import FormObject, STANDARD_MARGIN

class Input(FormObject):
    ''' Creates a TextInput object with a Text object label '''
    def __init__(self, label, value='', **kwargs):
        # Initialise as a form object
        FormObject.__init__(self, value)
        # Separate kwargs
        label_kwargs = dict([(k, v) for k, v in kwargs.iteritems() if k.startswith('label_')])
        input_kwargs = dict([(k, v) for k, v in kwargs.iteritems() if k.startswith('input_')])
        # Create objects
        self._label = Text(label, **label_kwargs)
        self._input = TextInput(value, **input_kwargs)
        # Default box styles
        self.style = {
            # Appearance
            'border_width'    : 0,
            'border_color'    : (0, 0, 0),
            'bg_color'        : (255, 255, 255, 0),
            # Position
            'position'        : 'relative',
            'top'            : STANDARD_MARGIN[1] // 2,
            'bottom'        : STANDARD_MARGIN[1] // 2,
            'left'            : STANDARD_MARGIN[0] // 2,
            'right'            : STANDARD_MARGIN[0] // 2
        }
        # Apply custom box styles
        for s, v in kwargs.iteritems():
            if s in self.style:
                self.style[s] = v

    def _reset(self):
        # Restore value to default
        self._input._reset()

    def update(self, e):
        # Send events straight to input
        return self._input.update(e)

    def focus(self):
        # Give both focus states
        self._label.focus()
        self._input.focus()

    def blur(self):
        # Remove focus states
        self._label.blur()
        self._input.blur()

    def get_surface(self):
        # Get child surfaces and their sizes
        l = self._label.get_surface()
        i = self._input.get_surface()
        sl, si = l.get_size(), i.get_size()
        # Get own dimensions
        padding = 10 # pixels
        width = sl[0] + padding + si[0]
        height = max(sl[1], si[1])
        # Create own surface
        surf = pygame.Surface((width, height)).convert_alpha()
        surf.fill((0, 0, 0, 0)) # Transparent
        # Add child surfaces v-centered
        surf.blit(l, (0, (height - sl[1]) // 2 + 1))
        surf.blit(i, (width - si[0], (height - si[1]) // 2))
        return surf

    def value(self):
        return self._input.value()
