from .socket import Socket
from .acceptor_socket import AcceptorSocket
import logging
import signal
import sys

from .server_protocol import ServerProtocol


class Server:
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
        """
        Dummy Server loop

        Server that accept a new connections and establishes a
        communication with a client. After client with communucation
        finishes, servers starts to accept new connections again
        """

        # Modify this program to handle signal to graceful shutdown
        # the server

        while True:
            self._client_sock = self.__accept_new_connection()
            self.__handle_client_connection()

    def __handle_client_connection(self):
        """
        Read message from a specific client socket and closes the socket

        If a problem arises in the communication with the client, the
        client socket will also be closed
        """
        try:
            protocol = ServerProtocol()
            protocol.recv_bet(self._client_sock)
            addr = self._client_sock.getpeername()
            logging.info(f'action: receive_message | result: success | ip: {addr[0]} ')
            protocol.send_ok(self._client_sock)
        except OSError as e:
            logging.error("action: receive_message | result: fail | error: {e}")
        finally:
            self._client_sock.shutdown_and_close()
            self._client_sock = None

    def __accept_new_connection(self):
        """
        Accept new connections

        Function blocks until a connection to a client is made.
        Then connection created is printed and returned
        """

        # Connection arrived
        logging.info('action: accept_connections | result: in_progress')
        c = self._acceptor_socket.accept()
        #TODO verify if accept returns a peer socket addr or acceptor addr
        logging.info(f'action: accept_connections | result: success | ip: {c.get_addr()}')
        return c
