from multiprocessing import Lock
from .utils import store_bets, load_bets

class BetsDBMonitor:
    def __init__(self):
        self._lock = Lock()

    def store_bets(self, bets):
        self._lock.acquire()
        store_bets(bets)
        self._lock.release()


    def load_bets(self):
        # All agencies finished writing so there is no need to lock
        return load_bets()
