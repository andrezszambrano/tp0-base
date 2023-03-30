import datetime
import logging
import signal
import sys
import time
from .client_protocol import ClientProtocol
from .socket_wrapper import Socket


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
        self._socket = Socket(self._host, self._port)
        self.__send_agency_number()
        for batch in batches:
            self.__send_batch_to_server(batch)
        self.__send_finished_message_to_server()
        self.__recv_agency_winners()

    def __send_batch_to_server(self, batch):
        try:
            protocol = ClientProtocol()
            protocol.send_batch(self._socket, batch)
            protocol.recv_ok(self._socket)
            logging.debug("action: batch_enviado | result: success")
        except OSError as e:
            logging.error(f"action: connect | result: fail | client_id: {self._id} | error: {e}")

    def __send_finished_message_to_server(self):
        try:
            protocol = ClientProtocol()
            protocol.send_finished_message(self._socket)
            protocol.recv_ok(self._socket)
            logging.info("action: agencia_registrada_como_finalizada | result: success")
        except OSError as e:
            logging.error(f"action: connect | result: fail | client_id: {self._id} | error: {e}")

    def __recv_agency_winners(self):
        try:
            while True:
                protocol = ClientProtocol()
                winners = protocol.try_to_recv_winners_documents(self._socket)
                if winners != None:
                    logging.info(f"action: consulta_ganadores | result: success | cant_ganadores: ${len(winners)}")
                    break
        except OSError as e:
            logging.error(f"action: connect | result: fail | client_id: {self._id} | error: {e}")

    def __generate_bets_batchs(self, bets, batch_size):
        return [bets[i:i + batch_size] for i in range(0, len(bets), batch_size)]

    def __send_agency_number(self):
        try:
            protocol = ClientProtocol()
            protocol.send_agency_number(self._socket, self._id)
        except OSError as e:
            logging.error(f"action: connect | result: fail | client_id: {self._id} | error: {e}")

