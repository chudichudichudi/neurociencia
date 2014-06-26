import pygame
from multineuro.forms.form_object import FormObject
class Frame(FormObject):
    def __init__(self, size, position, **kwargs):
        # Initialise as a form object
        FormObject.__init__(self, None)
        self._tab_skip = True
        # Store some info
        self.position = position
        self._objects = {}
        self._index = {}
        # Default box styles
        self.style = {
            # Appearance
            'border_width'    : 0,
            'border_color'    : (0, 0, 0),
            'bg_color'        : (255, 255, 255, 0),
            # Size
            'height'        : size[1],
            'width'            : size[0],
            # Position
            'position'        : 'absolute',
            'top'            : position[1],
            'bottom'        : 0,
            'left'            : position[0],
            'right'            : 0
        }
        # Apply custom box styles
        for s, v in kwargs.iteritems():
            if s in self.style:
                self.style[s] = v

    def value(self):
        return None

    def add_object(self, name, obj, index=None):
        ''' Add object to Form with reference "name". '''
        if name not in self._objects:
            # Reference as child
            obj._in_frame = self
            # Add object reference
            self._objects[name] = obj
            # Add object index
            if not index or index >= len(self._index):
                self._index[len(self._index)] = name
            else:
                for i in xrange(index, len(self._index) - 1):
                    self._index[i + 1] = self._index[i]
                self._index[index] = name
        else:
            raise ValueError, 'Form object already contains a(n) "%s" object' % name

#    def rem_object(self, name):
#        ''' Removes object initialized with "name" from the form.\n\nN.B. This is currently a slow, cpu heavy, operation. '''
#        if name in self._objects:
#            # Delete object
#            self._objects.__delitem__(name)
#            # Update indexes
#            x = dict([(v, k) for (k, v) in self._index.iteritems()])[name]
#            for i in xrange(x + 1, len(self._index) - 1):
#                self._index[i] = self._index[i + 1]
#            # Remove index
#            self._index.__delitem__(i + 1)
#            # Check that the removed item wasn't selected
#            if self._selected >= len(self._index):
#                self._selected = len(self._index) - 1
#        else:
#            raise KeyError, 'Form object does not contain a(n) "%s" object' % name

    def get_surface(self):
        # Make sure the frame has objects
        if not len(self._objects):
            raise AttributeError, 'Frame has no objects.'
        surf = pygame.Surface((self.style['height'], self.style['width'])).convert_alpha()
        surf.fill(self.style['bg_color'])
        if self.style['border_width'] > 0:
            pygame.draw.rect(surf, self.style['border_color'], (0, 0, self.style['width'] - self.style['border_width'] // 2, self.style['height'] - self.style['border_width'] // 2), self.style['border_width'])
        c_y = self.style['border_width']
        for i in xrange(0, len(self._objects)):
            o = self._objects[self._index[i]]
            s = o.get_surface()
            surf.blit(s, (o.style['left'], c_y + o.style['top']))
            c_y += o.style['top'] + s.get_height() + o.style['bottom']
        return surf
