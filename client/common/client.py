import socket
import logging
import signal
import sys
import time

class Client:
    def __init__(self, id, server_address, loop_lapse, loop_period):
        # Initialize server socket
        self._id = id
        self._host, port = server_address.split(':')
        self._port = int(port)
        self._loop_lapse = loop_lapse
        self._loop_period = loop_period
        self._client_socket = None
        signal.signal(signal.SIGTERM, self.__exit_gracefully)

    def __exit_gracefully(self, signum, frame):
        if self._client_socket != None:
            self._client_socket.shutdown(socket.SHUT_RDWR)
            self._client_socket.close()
            logging.info(f'action: client socket closed | result: success')
        logging.info(f'action: sigterm detected, client shutdowned | result: success')
        sys.exit(0)

    def __timeout_handler(self, signum, frame):
        if self._client_socket != None:
            self._client_socket.shutdown(socket.SHUT_RDWR)
            self._client_socket.close()
        logging.info(f"action: timeout_detected | result: success | client_id: {self._id}")
        sys.exit(0)

    def run(self):
        signal.signal(signal.SIGALRM, self.__timeout_handler)
        signal.alarm(self._loop_lapse)

        msg_id = 1
        while True:
            self.__connect_and_message_server(msg_id)
            msg_id = msg_id + 1
            time.sleep(self._loop_period)

    def __connect_and_message_server(self, msg_id):
        try:
            self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._client_socket.connect((self._host, self._port))
            self.__send_message_to_server(msg_id)

            self._client_socket.shutdown(socket.SHUT_RDWR)
            self._client_socket.close()
            self._client_socket = None
        except OSError as e:
            logging.error(f"action: connect | result: fail | client_id: {self._id} | error: {e}")

    def __send_message_to_server(self, msg_id):
        try:
            self._client_socket.send("[CLIENT {}] Message N°{}".format(self._id, msg_id).encode('utf-8'))
            msg = self._client_socket.recv(1024).rstrip().decode('utf-8')
            logging.info(f"action: receive_message | result: success | client_id: {self._id} | msg: {msg}")
        except OSError as e:
            logging.error(f"action: receive_message | result: fail | client_id: {self._id} | error: {e}")
