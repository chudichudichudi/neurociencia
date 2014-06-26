""" Contains Tips object. """
from cleaner import Cleaner
from fetcher import Fetcher
from tip import Tip
from threading import Lock
from threads import wait_free_acquire

class Tips(object):
    """ Manage Tips Events. """

    def __init__(self, enable):
        self.enable = enable
        self._tips = {}
        self._new_tips = set()
        self.lock = Lock()
        if self.enable:
            self.fetcher = Fetcher(self._tips, self.lock, self._new_tips)
            self.cleaner = Cleaner(self._tips, self.lock, self._new_tips)
            self.fetcher.start()
            self.cleaner.start()

    def tips(self):
        return self._tips.values()

    def new_tips(self):
        if self._new_tips:
            wait_free_acquire(self.lock)
            res = [self._tips[x] for x in self._new_tips]
            self._new_tips.clear()
            self.lock.release()
            return res
        else:
            return []

    def stop(self):
        if self.enable:
            self.fetcher.finnish()
            self.cleaner.finnish()

