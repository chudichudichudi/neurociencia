""" Contains Fetcher class and it configuration. """
from threads import Looper, wait_free_acquire
#import tuio
import time
from multineuro.tips.tip import Tip

UPDATE_PER_SECOND_FETCHER = 80

class Fetcher(Looper):
    """ tips Producer.
    Deposita o actualiza tips en un diccionario"""

    def __init__(self, tips, lock, new_tips):
        super(Fetcher, self).__init__()
        self.tips = tips
        self.lock = lock
        self.new_tips = new_tips
        self.tracking = tuio.Tracking()

    def main(self):
        self.tracking.update()
        # pylint: disable=E1101
        for obj in self.tracking.cursors():
            self._store(obj)
        # pylint: enable=E1101
        time.sleep(1.0 / UPDATE_PER_SECOND_FETCHER)

    def _store(self, cursor2d):
        ide = cursor2d.sessionid
        wait_free_acquire(self.lock)
        if ide in self.tips:
            self.tips[ide].update()
        else:
            self.tips[ide] = Tip(cursor2d)
            self.new_tips.add(ide)
        self.lock.release()

    def finnish(self):
        self.tracking.stop()
        super(Fetcher, self).finnish()
