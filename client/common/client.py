import datetime
import logging
import signal
import sys
import time
from .client_protocol import ClientProtocol
from .socket import Socket


class Client:
    def __init__(self, id, server_address, loop_lapse, loop_period):
        # Initialize server socket
        self._id = id
        self._host, port = server_address.split(':')
        self._port = int(port)
        self._loop_lapse = loop_lapse
        self._loop_period = loop_period
        self._socket = None
        signal.signal(signal.SIGTERM, self.__exit_gracefully)

    def __exit_gracefully(self, signum, frame):
        if self._socket != None:
            self._socket.shutdown_and_close()
            logging.info(f'action: client socket closed | result: success')
        logging.info(f'action: sigterm detected, client shutdowned | result: success')
        sys.exit(0)

    def __timeout_handler(self, signum, frame):
        if self._socket != None:
            self._socket.shutdown_and_close()
        logging.info(f"action: timeout_detected | result: success | client_id: {self._id}")
        sys.exit(0)

    def run(self, bets):
        signal.signal(signal.SIGALRM, self.__timeout_handler)
        signal.alarm(self._loop_lapse)
        for bet in bets:
            self.__connect_and_send_bet_to_server(bet)

    def __connect_and_send_bet_to_server(self, bet):
        try:
            self._socket = Socket(self._host, self._port)
            protocol = ClientProtocol()
            protocol.send_bet(self._socket, bet)#"Andres", "Zambrano", 30904465, datetime.datetime.now(), 12345)
            protocol.recv_ok(self._socket)
            logging.info("action: apuesta_enviada | result: success | dni: $30904465 | numero: $12345")
            self._socket.shutdown_and_close()
            self._socket = None
        except OSError as e:
            logging.error(f"action: connect | result: fail | client_id: {self._id} | error: {e}")

    def __send_message_to_server(self, protocol, msg_id):
        try:
            protocol.send_default_message(self._socket, self._id, msg_id)
            msg = protocol.recv_message(self._socket)
            logging.info(f"action: receive_message | result: success | client_id: {self._id} | msg: {msg}")
        except OSError as e:
            logging.error(f"action: receive_message | result: fail | client_id: {self._id} | error: {e}")
