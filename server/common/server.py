from .socket import Socket
from .acceptor_socket import AcceptorSocket
from .bet import Bet
import logging
import signal
import sys

from .server_protocol import ServerProtocol
from .utils import store_bets, load_bets, has_won


class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self._acceptor_socket = AcceptorSocket('', port, listen_backlog)
        self._client_sock = None
        signal.signal(signal.SIGTERM, self.__exit_gracefully)
        self._clients_dict = {}

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
            action = protocol.recv_char(self._client_sock)
            if action == protocol.START_BATCH:
                self.__recv_batch_from_client(protocol)
            elif action == protocol.FINISHED_CHAR:
                self.__save_agency_as_finished(protocol)
            else:
                agency_number = protocol.recv_agency_number(self._client_sock)
                if self.__all_agencies_finished():
                    protocol.send_ok(self._client_sock)
                    self.__load_bets_and_send_agency_winners(protocol, agency_number)
                else:
                    protocol.send_forbidden(self._client_sock)

        except OSError as e:
            logging.error(f"action: receive_message | result: fail | error: {e}")
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
        logging.info(f'action: accept_connections | result: success | ip: {c.getpeername()[0]}')
        return c

    def __recv_batch_from_client(self, protocol):
        bets = protocol.recv_bets_batch(self._client_sock)
        store_bets(bets)
        self._clients_dict[bets[0].agency] = False
        logging.debug(f"action: batch_almacenado | result: success")
        protocol.send_ok(self._client_sock)

    def __save_agency_as_finished(self, protocol):
        agency_number = protocol.recv_agency_number(self._client_sock)
        self._clients_dict[agency_number] = True
        if self.__all_agencies_finished():
            logging.info("action: sorteo | result: success")

    def __all_agencies_finished(self):
        return all(value == True for value in self._clients_dict.values())


    def __load_bets_and_send_agency_winners(self, protocol, agency_number):
        bets = load_bets()
        agency_winners = filter(lambda bet: has_won(bet) & bet.agency == agency_number, bets)
        protocol.send_agency_winners_documents(self._client_sock, agency_winners)