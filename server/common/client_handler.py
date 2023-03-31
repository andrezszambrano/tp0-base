import logging

from .server_protocol import ServerProtocol
from .utils import has_won

REGISTER = "R"
NEW_SOCKET = "S"
FINALIZED_AGENCY = "F"


class ClientHandler:
    def __init__(self, client_socket, queue, clients_map, bets_monitor):
        self._client_sock = client_socket
        self._queue = queue
        self._clients_map = clients_map
        self._bets_monitor = bets_monitor

    def run(self):
        protocol = ServerProtocol()
        self._agency_number = protocol.recv_agency_number(self._client_sock)
        self._finished = False
        while not self._finished:
            self.__handle_client_connection()

        self._client_sock.shutdown_and_close()
        self._client_sock = None
        self._queue.put((FINALIZED_AGENCY, ))

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
                if self._clients_map.all_agencies_finished():
                    logging.debug(f"Se regresa ganadores de la agencia {self._agency_number}")
                    protocol.send_ok(self._client_sock)
                    self.__load_bets_and_send_agency_winners(protocol)
                    self._finished = True
                else:
                    protocol.send_forbidden(self._client_sock)

        except OSError as e:
            logging.error(f"action: receive_message | result: fail | error: {e}")


    def __recv_batch_from_client(self, protocol):
        bets = protocol.recv_bets_batch(self._client_sock, self._agency_number)
        self._bets_monitor.store_bets(bets)
        logging.debug(f"action: batch_almacenado | result: success")
        protocol.send_ok(self._client_sock)

    def __save_agency_as_finished(self, protocol):
        self._clients_map.set_agency_finished(self._agency_number)
        protocol.send_ok(self._client_sock)

    def __load_bets_and_send_agency_winners(self, protocol):
        bets = self._bets_monitor.load_bets()
        agency_winners = filter(lambda bet: has_won(bet) and bet.agency == self._agency_number,
                                bets)
        protocol.send_agency_winners_documents(self._client_sock, agency_winners)

