STANDARD_MARGIN = (20, 20)    # Pixels
SCROLL_BAR_WIDTH = 10        # Pixels

class FormObject(object):
    def __init__(self, value):
        self._value = self._default = value
        self._has_focus = False
        self._tab_skip = False
        self._in_frame = None

    def _reset(self):
        """ Restore value to default """
        self._value = self._default

    def update(self, _):
        """Deal with events"""
        return True

    def focus(self):
        """ When the object gains focus"""
        self._has_focus = True

    def blur(self):
        """ When the object loses focus"""
        self._has_focus = False
