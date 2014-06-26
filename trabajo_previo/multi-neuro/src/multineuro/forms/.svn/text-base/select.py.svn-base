from multineuro.forms.form_object import FormObject, STANDARD_MARGIN, \
    SCROLL_BAR_WIDTH
import pygame

class Select(FormObject):
    def __init__(self, value= -1, font=None, size=22, color=(0, 0, 0), style=[], **kwargs):
        # Initialise as a form object
        FormObject.__init__(self, value)
        # Create internals
        self._options = {}
        self._index = {}
        self._is_active = False
        # Create font
        if isinstance(font, pygame.font.Font):
            self._font = font
        else:
            self._font = pygame.font.Font(font, int(size))
            self._size = size
        # Style font
        self._color = color
        self._style = style
        for s in style:
            if s == 'bold' : self._font.set_bold(True)
            elif s == 'italic' : self._font.set_italic(True)
            elif s == 'underline' : self._font.set_underline(True)
        # Default box styles
        self.style = {
            # Appearance
            'border_width'    : 1,
            'border_color'    : (0, 0, 0),
            'scroll_color'    : (105, 0, 205),
            'bg_color'        : (255, 255, 255),
            'bg_focus_color': (205, 155, 255),
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
            if s in self.style:
                self.style[s] = v

    def _cursor_up(self):
        # Move cursor down
        if self._value > 0:
            self._value -= 1

    def _cursor_down(self):
        # Move cursor up
        if self._value < len(self._index) - 1:
            self._value += 1

    def add_option(self, name, value, index=None, **kwargs):
        for k in ['font', 'color', 'style']:
            if k not in kwargs:
                kwargs[k] = getattr(self, '_' + k)
        if name not in self._options:
            # Add object reference
            self._options[name] = SelectOption(name, value, **kwargs)
            # Add object index
            if not index or index >= len(self._index):
                self._index[len(self._index)] = name
            else:
                for i in xrange(index, len(self._index) - 1):
                    self._index[i + 1] = self._index[i]
                self._index[index] = name
            # Adjust size for new text
            tw, th = self._options[name]._font.size(name)
            # Adjust constraints to fit text
            self.style['width'] = max(self.style['width'], STANDARD_MARGIN[0] // 2 + tw + 4 + self.style['border_width'] * 2 + SCROLL_BAR_WIDTH)
            self.style['height'] = max(self.style['height'], th + 4 + self.style['border_width'])
            # Determine padding
            self._padding = (
                STANDARD_MARGIN[0] // 2,
                #(self.style['width'] - tw)//2 + self.style['border_width'],
                (self.style['height'] - th) // 2 + self.style['border_width'])
        else:
            raise ValueError, 'Select object already contains a(n) "%s" option' % name

    def rem_option(self, name):
        if name in self._options:
            # Delete object
            self._options.__delitem__(name)
            # Update indexes
            x = dict([(v, k) for (k, v) in self._index.iteritems()])[name]
            for i in xrange(x + 1, len(self._index) - 1):
                self._index[i] = self._index[i + 1]
            # Remove index
            self._index.__delitem__(i + 1)
            # Check that the removed item wasn't selected
            if self._value >= len(self._index):
                self._value = len(self._index) - 1
        else:
            raise KeyError, 'Select object does not contain a(n) "%s" option' % name

    def update(self, e):
        # Default: event used
        r = False
        # Control events when self has focus
        if e.type == pygame.locals.KEYDOWN:
            key = pygame.key.name(e.key)
            # Switch activity
            if e.key == pygame.locals.K_RETURN:
                self._is_active ^= True
            # Move cursor
            elif key == 'up' and self._is_active:
                self._cursor_up()
            elif key == 'down' and self._is_active:
                self._cursor_down()
            # Signal event unused
            else:
                r = True
        else:
            r = True
        return r

    def get_surface(self):
        # Make sure the object has options
        if not len(self._options):
            raise AttributeError, 'Select has no options.'
        # Create side-arrow
        arrow = pygame.Surface((self.style['height'] - self.style['border_width'], self.style['height']))
        # Fill and border
        arrow.fill((200, 200, 200))
        if self.style['border_width'] > 0:
            pygame.draw.rect(arrow, self.style['border_color'], (-self.style['border_width'], 0, self.style['height'] - self.style['border_width'] // 2, self.style['height'] - self.style['border_width'] // 2), self.style['border_width'])
        # The arrow
        cw, ch = (s // 2 for s in arrow.get_size())
        cw -= self.style['border_width'] // 2
        ch += self.style['border_width'] // 2
        if self._is_active:
            points = [(cw + cw // 3, ch // 2), (cw // (3. / 2), ch), (cw + cw // 3, ch + ch // 2)]
        else:
            points = [(cw // 2, ch // (3. / 2)), (cw, ch + ch // 3), (cw + cw // 2, ch // (3. / 2))]
        pygame.draw.aalines(arrow, self.style['border_color'], False, points, 1)
        # Create surface
        if self._is_active:
            # Create ranges
            count = 5
            if len(self._index) < count:
                count = len(self._index)
                irange = (0, count)
            elif self._value < 2:
                irange = (0, count)
            elif self._value > len(self._index) - 3:
                irange = (len(self._index) - count, len(self._index))
            else:
                irange = (self._value - 2, self._value + 3)
            # Create box
            height = (self._font.get_linesize() + self._padding[1] * 2) * count
            box = pygame.Surface((self.style['width'] + self.style['height'] - self.style['border_width'], height)).convert_alpha()
            box.fill((0, 0, 0, 0))
            # Add box
            pygame.draw.rect(box, self.style['bg_color'], (0, 0, self.style['width'], height))
            if self.style['border_width'] > 0:
                pygame.draw.rect(box, self.style['border_color'], (0, 0, self.style['width'] - self.style['border_width'] // 2, height - self.style['border_width'] // 2), self.style['border_width'])
            # Create hilight
            hilight = pygame.Surface((self.style['width'] - (3 * self.style['border_width'] + SCROLL_BAR_WIDTH), self.style['height']))
            hilight.fill(self.style['bg_focus_color'])
            # Scroll bar
            sx = self.style['width'] - (SCROLL_BAR_WIDTH // 2 + self.style['border_width'] // 2 * 3)
            sp = (height - 2.*self.style['border_width']) / len(self._index)
            lx = self.style['width'] - SCROLL_BAR_WIDTH - self.style['border_width'] * 2
            pygame.draw.line(box, self.style['border_color'], (lx, 0), (lx, height), self.style['border_width'])
            pygame.draw.line(box, self.style['scroll_color'], (sx, sp * irange[0] + self.style['border_width']), (sx, sp * irange[1] + self.style['border_width'] // 2), SCROLL_BAR_WIDTH)
            # Create text
            cy = self._padding[1] + self.style['border_width']
            for i in xrange(*irange):
                # Hilight
                if i == self._value:
                    box.blit(hilight, (self.style['border_width'], cy - self._padding[1]))
                # Text
                text = self._options[self._index[i]].get_surface()
                box.blit(text, (self._padding[0], cy))
                cy += self._font.get_linesize() + self._padding[1] * 2
        else:
            # Create text
            if self._value >= 0:
                text = self._options[self._index[self._value]].get_surface()
            else:
                text = None
            box = pygame.Surface((self.style['width'] + self.style['height'] - self.style['border_width'], self.style['height'])).convert_alpha()
            # Add box
            box.fill((self.style['bg_color'], self.style['bg_focus_color'])[self._has_focus])
            if self.style['border_width'] > 0:
                pygame.draw.rect(box, self.style['border_color'], (0, 0, self.style['width'] - self.style['border_width'] // 2, self.style['height'] - self.style['border_width'] // 2), self.style['border_width'])
            # Add text to box [centered H & V]
            if text:
                box.blit(text, self._padding)
        # Add arrow to main surface
        box.blit(arrow, (self.style['width'], (box.get_height() - arrow.get_height()) // 2))
        return box

    def value(self):
        if self._value >= 0:
            return self._options[self._index[self._value]]._value
        else:
            return None


class SelectOption(FormObject):
    def __init__(self, name, value, font=None, size=22, color=(0, 0, 0), style=[]):
        # Store some info
        self._name = name
        self._value = value
        # Create font
        if isinstance(font, pygame.font.Font):
            self._font = font
        else:
            self._font = pygame.font.Font(font, int(size))
        # Style font
        self._color = color
        for s in style:
            if s == 'bold' : self._font.set_bold(True)
            elif s == 'italic' : self._font.set_italic(True)
            elif s == 'underline' : self._font.set_underline(True)

    def get_surface(self):
        return self._font.render(self._name, True, self._color)
