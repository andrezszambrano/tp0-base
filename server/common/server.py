from multiprocessing import Process, SimpleQueue
from time import sleep

import logging
import signal
import sys

from .bets_db_monitor import BetsDBMonitor
from .client_handler import *
from .clients_finished_map import ClientsFinishedMap
from .server_protocol import ServerProtocol
from .acceptor import Acceptor


class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self._client_sock = None
        self._acceptor = Acceptor(port, listen_backlog)
        signal.signal(signal.SIGTERM, self.__exit_gracefully)
        self._client_processes = []

    def __exit_gracefully(self, signum, frame):
        logging.info(f'closing')
        if self._client_sock != None:
            self._client_sock.shutdown_and_close()
            logging.info(f'action: client socket closed | result: success')

        logging.info(f'action: sigterm detected, server shutdowned | result: success')
        sys.exit(0)

    def run(self):
        """
        Dummy Server loop

        Server that accept a new connections and establishes a
        communication with a client. After client with communucation
        finishes, servers starts to accept new connections again
        """

        # Modify this program to handle signal to graceful shutdown
        # the server

        queue = SimpleQueue()
        clients_map = ClientsFinishedMap()
        bets_monitor = BetsDBMonitor()
        acceptor_process = Process(target=self._acceptor.run, args=(queue,), daemon=True)
        acceptor_process.start()

        while True:
            message = queue.get()
            if message[0] == NEW_SOCKET:
                client_process = self.__create_and_start_client_handler_process(
                    queue, message[1], clients_map, bets_monitor)
                self._client_processes.append(client_process)
            if message[0] == FINALIZED_AGENCY:
                if clients_map.all_agencies_finished():
                    break

        acceptor_process.terminate()
        acceptor_process.join()
        for client_process in self._client_processes:
            client_process.join()

    def __create_and_start_client_handler_process(self, queue, agency_number, clients_map,
                                                  bets_monitor):
        client_handler = ClientHandler(agency_number, queue, clients_map, bets_monitor)
        client_process = Process(target=client_handler.run, args=(),
                                 daemon=True)
        client_process.start()
        return client_process

