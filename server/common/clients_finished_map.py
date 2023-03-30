from multiprocessing import Lock


class ClientsFinishedMap:

    def __init__(self):
        self._lock = Lock()
        self._clients_dict = {}

    def all_agencies_finished(self):
        self._lock.acquire()
        finished = all(value == True for value in self._clients_dict.values())
        self._lock.release()
        return finished

    def set_agency_finished(self, agency_number):
        self._lock.acquire()
        self._clients_dict[agency_number] = True
        self._lock.release()
