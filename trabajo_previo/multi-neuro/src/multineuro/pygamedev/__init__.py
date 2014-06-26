from multineuro.pygamedev.points import Points
from multineuro.tips import Tips


class PygameTips(Tips):

    def __init__(self, tuio=True):
        super(PygameTips, self).__init__(tuio)
        self.points = Points(self._new_tips, self._tips, self.lock)

    def initialize(self):
        self.points.start()
