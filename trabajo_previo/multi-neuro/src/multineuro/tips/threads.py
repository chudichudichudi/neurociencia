from threading import Thread, current_thread
import time
from abc import abstractmethod, ABCMeta
class Looper(Thread):
    __metaclass__ = ABCMeta
    def __init__(self):
        super(Looper, self).__init__()
        self.termino = False
        self.name = 'multi.' + self.name

    def run(self):
        while not self.termino:
            self.main()

    @abstractmethod
    def main(self):
        pass


    def finnish(self):
        if current_thread().ident == self.ident:
            raise Exception("Absurd! call finnish it's not neccessary")
        self.termino = True
        self.join(0.2)

def wait_free_acquire(lock):
    while not lock.acquire(False):
        time.sleep(0)
