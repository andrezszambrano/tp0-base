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

    def handler(self, signum, frame):
        print("Forever is over!")
        raise Exception("end of time")

    def run(self):
        signal.signal(signal.SIGALRM, self.handler)
        signal.alarm(self._loop_lapse)

        msg_id = 1
        while True:
            logging.debug(f"MSG { msg_id }")
            self.connect_and_message_server(msg_id)
            msg_id = msg_id + 1
            time.sleep(self._loop_period)

    def connect_and_message_server(self, msg_id):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self._host, self._port))
            client_socket.send("[CLIENT {}] Message N°{}".format(self._id, msg_id).encode('utf-8'))
            msg = client_socket.recv(1024).rstrip().decode('utf-8')
            logging.info(f"action: receive_message | result: success | client_id: {self._id} | msg: {msg}")
        except OSError as e:
            logging.error("action: receive_message | result: fail | error: {e}")
        finally:
            client_socket.close()
