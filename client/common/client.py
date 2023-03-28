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

    def run(self, bets, batch_size):
        signal.signal(signal.SIGALRM, self.__timeout_handler)
        signal.alarm(self._loop_lapse)
        batches = self.__generate_bets_batchs(bets, batch_size)
        for batch in batches:
            self.__connect_and_send_batch_to_server(batch)
        self.__send_finished_message_to_server()
        self.__recv_agency_winners()
    def __connect_and_send_batch_to_server(self, batch):
        try:
            self._socket = Socket(self._host, self._port)
            protocol = ClientProtocol()
            protocol.send_batch(self._socket, batch)
            protocol.recv_ok(self._socket)
            logging.debug("action: batch_enviado | result: success")
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

    def __send_finished_message_to_server(self):
        try:
            self._socket = Socket(self._host, self._port)
            protocol = ClientProtocol()
            protocol.send_finished_message(self._socket, self._id)
            protocol.recv_ok(self._socket)
            logging.debug("action: agencia_registrada_como_finalizada | result: success")
            self._socket.shutdown_and_close()
            self._socket = None
        except OSError as e:
            logging.error(f"action: connect | result: fail | client_id: {self._id} | error: {e}")

    def __recv_agency_winners(self):
        try:
            while True:
                self._socket = Socket(self._host, self._port)
                protocol = ClientProtocol()
                winners = protocol.try_to_recv_winners_documents(self._socket, self._id)
                if winners != None:
                    logging.debug(f"action: consulta_ganadores | result: success | cant_ganadores: ${len(winners)}")
                    break
                self._socket.shutdown_and_close()
                self._socket = None
        except OSError as e:
            logging.error(f"action: connect | result: fail | client_id: {self._id} | error: {e}")

    def __generate_bets_batchs(self, bets, batch_size):
        return [bets[i:i + batch_size] for i in range(0, len(bets), batch_size)]
