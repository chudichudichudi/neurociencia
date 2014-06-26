#!/opt/local/bin/python2.6
# Copyright 2009 Jeremy Worboys <jemthealmighty@gmail.com>
# Licensed for distribution under the GPL version 3
#
# TODO:
#         [ ] Write documentation for most objects/methods.
#         [ ] Clean up `get_suface` method for most objects.
#        [ ] Move kwarg styling to object `style` property
#         [ ] Integrate `style` property as part of `FormObject`
#                rather than individual objects.
#         [ ] Find and fix any bottle-necks.
#         [ ] Major error checking.

import pygame
import pygame.locals as PL
from multineuro.forms.select import Select
from multineuro.forms.frame import Frame

class Form(object):
    def __init__(self, auto_submit=True):
        self._auto_submit = auto_submit
        self._objects = {}
        self._index = {}
        self._selected = 0

    def _next(self):
        o = self._objects[self._index[self._selected]]
        if not isinstance(o, Select) or not o._is_active:
            o.blur()
            if self._selected + 1 in self._index:
                self._selected += 1
            else:
                self._selected = 0
            o = self._objects[self._index[self._selected]]
            o.focus()
        if o._tab_skip:
            self._next()

    def _previous(self):
        o = self._objects[self._index[self._selected]]
        if not isinstance(o, Select) or not o._is_active:
            o.blur()
            if self._selected - 1 in self._index:
                self._selected -= 1
            else:
                self._selected = len(self._index) - 1
            o = self._objects[self._index[self._selected]]
            o.focus()
        if o._tab_skip:
            self._previous()

    def _draw(self, screen):
        # Make sure the form has objects
        if not len(self._objects):
            raise AttributeError, 'Form has no objects.'
        screen.fill((200, 200, 200))
        c_y = 20
        blit_top = None
        for i in xrange(0, len(self._objects)):
            o = self._objects[self._index[i]]
            if o._in_frame:
                continue
            s = o.get_surface()
            if isinstance(o, Select) and o._is_active:
                blit_top = [s, (o.style['left'], o.style['top'] + c_y - (s.get_height() - o.style['height']) // 2)]
                c_y += o.style['top'] + o.style['height'] + o.style['bottom']
            else:
                if o.style['position'] == 'absolute':
                    screen.blit(s, (o.style['left'], o.style['top']))
                else:
                    screen.blit(s, (o.style['left'], c_y + o.style['top']))
                    c_y += o.style['top'] + s.get_height() + o.style['bottom']
        if blit_top:
            screen.blit(*blit_top)
        pygame.display.flip()

    def clear(self):
        # Restore all values to default
        for _, obj in self._objects.iteritems():
            obj._reset()

    def submit(self):
        # Stop running
        self._running = False

    def add_object(self, name, obj, index=None):
        ''' Add object to Form with reference "name". '''
        if name not in self._objects:
            # Add object reference
            self._objects[name] = obj
            # Add object index
            if not index or index >= len(self._index):
                index = len(self._index)
                self._index[index] = name
            else:
                for i in xrange(index, len(self._index) - 1):
                    self._index[i + 1] = self._index[i]
                self._index[index] = name
            # Add all containing objects
            if isinstance(obj, Frame):
                for j in xrange(len(obj._index)):
                    n = obj._index[j]
                    self.add_object(n, obj._objects[n], index + j + 1)
        else:
            raise ValueError, 'Form object already contains a(n) "%s" object' % name

    def rem_object(self, name):
        ''' Removes object initialized with "name" from the form.\n\nN.B. This is currently a slow, cpu heavy, operation. '''
        if name in self._objects:
            # Remove all containing objects
            if isinstance(self._objects[name], Frame):
                for _, n in self._objects[name]._index.iteritems():
                    self.rem_object(n)
            # Update parent
            parent = self._objects[name]._in_frame
            if parent:
                parent.rem_object(name)
            # Delete object
            self._objects.__delitem__(name)
            # Update indexes
            x = dict([(v, k) for (k, v) in self._index.iteritems()])[name]
            for i in xrange(x + 1, len(self._index) - 1):
                self._index[i] = self._index[i + 1]
            # Remove index
            self._index.__delitem__(i + 1)
            # Check that the removed item wasn't selected
            if self._selected >= len(self._index):
                self._selected = len(self._index) - 1
        else:
            raise KeyError, 'Form object does not contain a(n) "%s" object' % name

    def run(self, screen):
        ''' Displays the form on "screen" blocking the script until the form is 
        submitted.\nReturns a FormResult object. '''
        # Make sure the form has objects
        if not len(self._objects):
            raise AttributeError, 'Form has no objects.'
        # Loopdy-loop
        self._running = True
        self._draw(screen)
        while self._running:
            e = pygame.event.poll()
            if e.type == PL.KEYDOWN:
                # Move between objects
                if e.key == PL.K_TAB:
                    m = pygame.key.get_mods()
                    if m & PL.KMOD_LSHIFT or m & PL.KMOD_RSHIFT:
                        self._previous()
                    else:
                        self._next()
                    continue
                # Check whether selected object wants the event
                elif not self._objects[self._index[self._selected]].update(e):
                    continue
                # Submit form
                elif e.key == PL.K_RETURN and self._auto_submit:
                    self.submit()
                    continue
            # Draw the form
            self._draw(screen)
        result = {}
        for name, obj in self._objects.iteritems():
            if obj.value() is not None:
                result[name] = obj.value()
        return result

#     
# class Textarea(Input):
#     ''' Creates an Input object with multilines '''
#     def __init__(self, *args, **kwargs):
#         # Modify height for multiline [5 lines high]
#         if not 'input_height' in kwargs:
#             fs = (22, kwargs['input_size'])['input_size' in kwargs]
#             kwargs['input_height'] = (fs + 3)*5
#         # Make self an Input object
#         Input.__init__(self, *args, **kwargs)
#     



