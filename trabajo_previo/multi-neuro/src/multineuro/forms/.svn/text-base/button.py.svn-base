from multineuro.forms.form_object import FormObject, STANDARD_MARGIN
import pygame

class Button(FormObject):
    ''' A standard click -> function button [args is a tuple as if calling function]'''
    def __init__(self, value, function, args, font=None, size=22,
                 color=(50, 50, 50), focus_color=(0, 0, 0),
                 style=[], **kwargs):
        # Initialise as a form object
        FormObject.__init__(self, value)
        # Store data
        self._value = value
        self._function = function
        self._args = ((args,), args)[isinstance(args, tuple)]
        # Create font
        if isinstance(font, pygame.font.Font):
            self._font = font
        else:
            self._font = pygame.font.Font(font, int(size))
        # Style font
        self._color = color
        self._focus_color = focus_color
        for s in style:
            if s == 'bold' : self._font.set_bold(True)
            elif s == 'italic' : self._font.set_italic(True)
            elif s == 'underline' : self._font.set_underline(True)
        # Default box styles
        self.style = {
            # Appearance
            'border_width'    : 1,
            'border_color'    : (0, 0, 0),
            'bg_color'        : (255, 255, 255),
            'bg_focus_color': (205, 155, 255),
            # Size
            'height'        : 1,
            'width'            : 1,
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
        # Get rendered text height
        tw, th = self._font.size(self._value)
        # Adjust constraints to fit text
        self.style['width'] = max(self.style['width'],
                                  tw + 4 + self.style['border_width'])
        self.style['height'] = max(self.style['height'],
                                   th + 4 + self.style['border_width'])
        # Determine padding
        self._padding = (
            (self.style['width'] - tw) // 2 + self.style['border_width'],
            (self.style['height'] - th) // 2 + self.style['border_width'])

    def update(self, e):
        # Control events when self has focus
        if e.type == pygame.locals.KEYDOWN:
            # Enter/Return pressed -> run function
            if e.key == pygame.locals.K_RETURN:
                self.run()
                return False
        # Signal event unused
        return True

    def run(self):
        # Run the function with or without args
        if self._args:
            self._function(*self._args)
        else:
            self._function()

    def get_surface(self):
        # Create text
        text = self._font.render(self._value, True, (self._color, self._focus_color)[self._has_focus])
        # Create surface
        box = pygame.Surface((self.style['width'], self.style['height'])).convert_alpha()
        # Add box
        box.fill((self.style['bg_color'], self.style['bg_focus_color'])[self._has_focus])
        if self.style['border_width'] > 0:
            pygame.draw.rect(box,
                             self.style['border_color'],
                             (0, 0, self.style['width'] - self.style['border_width'] // 2,
                              self.style['height'] - self.style['border_width'] // 2),
                             self.style['border_width'])
        # Add text to box [centered H & V]
        box.blit(text, self._padding)
        return box

    def value(self):
        return None
