import logging
import signal
import sys

from acceptor_socket import AcceptorSocket


class Acceptor:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self._acceptor_socket = AcceptorSocket('', port, listen_backlog)
        self._client_sock = None
        signal.signal(signal.SIGTERM, self.__exit_gracefully)

    def __exit_gracefully(self, signum, frame):
        self._acceptor_socket.shutdown_and_close()
        logging.info(f'action: server socket closed | result: success')
        if self._client_sock != None:
            self._client_sock.shutdown_and_close()
            logging.info(f'action: client socket closed | result: success')

        logging.info(f'action: sigterm detected, server shutdowned | result: success')
        sys.exit(0)

    def run(self):
        p = self._acceptor_socket.accept()
        print("Acceptado!")
        p.shutdown_and_close()
