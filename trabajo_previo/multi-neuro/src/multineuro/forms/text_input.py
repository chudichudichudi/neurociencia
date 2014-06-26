import pygame, time
from multineuro.forms.form_object import FormObject, STANDARD_MARGIN

CURSOR_FLASH_SPEED = .7        # Seconds
KEY_REPEAT_DELAY = 500        # Milliseconds
KEY_REPEAT_INTERVAL = 150        # Milliseconds

class TextInput(FormObject):
    ''' A bare text input field, don't use this unless really needed '''
    def __init__(self, value='', max_chars=25, input_font=None, input_size=22, input_color=(0, 0, 0), input_style=[], **kwargs):
        # Initialise as a form object
        FormObject.__init__(self, value)
        # Store some information
        self._max_chars = max_chars
        self._cursor_pos = len(self._value)
        self._cursor_reset()
        # Create font
        if isinstance(input_font, pygame.font.Font):
            self._font = input_font
        else:
            self._font = pygame.font.Font(input_font, int(input_size))
        # Style font
        self._color = input_color
        for s in input_style:
            if s == 'bold' : self._font.set_bold(True)
            elif s == 'italic' : self._font.set_italic(True)
            elif s == 'underline' : self._font.set_underline(True)
        # Default box styles
        self.style = {
            # Appearance
            'border_width'    : 1,
            'border_color'    : (0, 0, 0),
            'bg_color'        : (255, 255, 255),
            # Size
            'height'        : 26,
            'width'            : 200,
            # Position
            'position'        : 'relative',
            'top'            : STANDARD_MARGIN[1] // 2,
            'bottom'        : STANDARD_MARGIN[1] // 2,
            'left'            : STANDARD_MARGIN[0] // 2,
            'right'            : STANDARD_MARGIN[0] // 2
        }
        # Apply custom box styles
        for s, v in kwargs.iteritems():
            # Remove 'input_'
            s = s[6:]
            if s in self.style:
                self.style[s] = v

    def _cursor_reset(self, on=True):
        # Update the next cursor switch and 
        self._cursor_switch = time.time() + CURSOR_FLASH_SPEED
        if on:
            self._cursor_on = True
        else:
            self._cursor_on ^= True

    def _cursor_forward(self):
        # Move cursor forwards
        if self._cursor_pos < len(self._value):
            self._cursor_pos += 1

    def _cursor_back(self):
        # Move cursor backwards
        if self._cursor_pos > 0:
            self._cursor_pos -= 1

    def _type_char(self, char):
        # Add a character behind the cursor
        if len(self._value) < self._max_chars:
            self._value = ''.join([
                    self._value[:self._cursor_pos],
                    char,
                    self._value[self._cursor_pos:]
                ])
            self._cursor_pos += 1

    def _backspace(self):
        # Remove the character behind the cursor
        if len(self._value) > 0:
            self._value = ''.join([
                    self._value[:self._cursor_pos - 1],
                    self._value[self._cursor_pos:]
                ])
            self._cursor_pos -= 1

    def update(self, e):
        r = False
        # Control events when self has focus
        if e.type == pygame.locals.KEYDOWN:
            key = pygame.key.name(e.key)
            ukey = e.unicode
            # Catch enter
            if key == 'return':
                return True
            # Move cursor
            elif key == 'left':
                self._cursor_back()
            elif key == 'right':
                self._cursor_forward()
            # Edit text
            elif key == 'backspace':
                self._backspace()
            elif key == 'space':
                self._type_char(' ')
            elif len(ukey) == 1:
                self._type_char(ukey)
            # Signal event unused
            else:
                r = True
            # Update cursor switch
            self._cursor_reset()
        else:
            r = True
        return r

    def focus(self):
        # When the object gets selected
        self._has_focus = True
        if self._value == self._default:
            self._value = ''
            self._cursor_pos = 0
        # Enable key repeating
        pygame.key.set_repeat(KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL)
        # Update cursor switch
        self._cursor_reset()

    def blur(self):
        # When the object loses focus
        self._has_focus = False
        if self._value.strip() == '':
            self._value = self._default
        # Disable key repeating
        pygame.key.set_repeat()

    def get_surface(self):
        # Create surface
        box = pygame.Surface((self.style['width'], self.style['height'])).convert_alpha()
        # Add box
        width = self.style['width'] + self.style['border_width'] * 2
        height = self.style['height'] + self.style['border_width'] * 2
        pygame.draw.rect(box, self.style['bg_color'], (0, 0, self.style['width'], self.style['height']))
        if self.style['border_width'] > 0:
            pygame.draw.rect(box, self.style['border_color'], (0, 0, self.style['width'] - self.style['border_width'] // 2, self.style['height'] - self.style['border_width'] // 2), self.style['border_width'])
        # Create text
        to_cursor = self._font.render(self._value[:self._cursor_pos], True, self._color)
        full_text = self._font.render(self._value, True, self._color)
        # Determine diplayed area
        tw, th = to_cursor.get_size()
        padding = (height - th) // 2 + 1
        offset = tw - self.style['width'] + 2 * padding
        offset = (int(offset), 0)[offset < 0]
        # Add text to box
        box.blit(full_text, (padding, padding), (offset, 0, self.style['width'] - 2 * padding, th))
        # Switch cursor
        if time.time() >= self._cursor_switch:
            self._cursor_reset(False)
        # Draw cursor
        if self._has_focus and self._cursor_on:
            pygame.draw.line(box, self.style['border_color'], (tw + padding - offset, padding // 2), (tw + padding - offset, th + padding))
        return box

    def value(self):
        return self._value
