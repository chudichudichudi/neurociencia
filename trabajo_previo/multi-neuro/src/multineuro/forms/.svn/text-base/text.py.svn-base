import pygame
from multineuro.forms.form_object import FormObject, STANDARD_MARGIN

class Text(FormObject):
    ''' Displays text on a form '''
    def __init__(self, value, label_font=None, label_size=22,
                 label_color=(0, 0, 0), label_style=[], **kwargs):
        # Initialise as a form object
        FormObject.__init__(self, value)
        self._tab_skip = True
        # Create font
        if isinstance(label_font, pygame.font.Font):
            self._font = label_font
        else:
            self._font = pygame.font.Font(label_font, int(label_size))
        # Style font
        self._color = label_color
        for s in label_style:
            if s == 'bold' : self._font.set_bold(True)
            elif s == 'italic' : self._font.set_italic(True)
            elif s == 'underline' : self._font.set_underline(True)
        # Default box styles
        self.style = {
            # Position
            'position'        : 'relative',
            'top'            : STANDARD_MARGIN[1] // 2,
            'bottom'        : STANDARD_MARGIN[1] // 2,
            'left'            : STANDARD_MARGIN[0] // 2,
            'right'            : STANDARD_MARGIN[0] // 2
        }
        # Apply custom box styles
        for s, v in kwargs.iteritems():
            # Remove 'label_'
            s = s[6:]
            if s in self.style:
                self.style[s] = v

    def get_surface(self):
        return self._font.render(self._value, True, self._color)

    def value(self):
        return None
