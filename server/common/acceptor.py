import logging
import signal
import sys

from .acceptor_socket import AcceptorSocket


class Acceptor:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self._acceptor_socket = AcceptorSocket('', port, listen_backlog)
        self._client_sock = None
        signal.signal(signal.SIGTERM, self.__exit_gracefully)

    def __exit_gracefully(self, signum, frame):
        self._acceptor_socket.shutdown_and_close()
        logging.info(f'action: server socket closed | result: success')
        sys.exit(0)

    def run(self, queue):
        while True:
            logging.info('action: accept_connections | result: in_progress')
            socket = self._acceptor_socket.accept()
            logging.info(f'action: accept_connections | result: success | ip: {socket.getpeername()[0]}')
            queue.put(("S", socket))
