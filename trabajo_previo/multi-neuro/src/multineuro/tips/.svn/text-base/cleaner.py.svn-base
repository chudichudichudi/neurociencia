from threads import Looper, wait_free_acquire
import time

UPDATE_PER_SECOND_CLEANER = 20

class Cleaner(Looper):
    """ Limpiador de tips.
    Borra tips expirados de un diccionario"""

    def __init__(self, tips, lock, new_tips):
        super(Cleaner, self).__init__()
        self.tips = tips
        self.new_tips = new_tips
        self.lock = lock


    def main(self):
        for tip in self.tips.values():
            if tip.expired():
                self._borrar(tip)
        time.sleep(1.0 / UPDATE_PER_SECOND_CLEANER)

    def _borrar(self, tip):
        wait_free_acquire(self.lock)
        self.tips[tip.ident].dispatch('finnish', self.tips[tip.ident])
        self.tips[tip.ident].delete()
        del self.tips[tip.ident]
        if tip.ident in self.new_tips:
            self.new_tips.remove(tip.ident)
        self.lock.release()
