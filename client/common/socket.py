import socket


class Socket:

    def __init__(self, host, port):
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.connect((host, port))
        self._socket = _socket

    def shutdown_and_close(self):
        self._socket.shutdown(socket.SHUT_RDWR)
        self._socket.close()

    def send(self, buffer, length):
        #sent = 0
        #while sent < length:
            #aux =\
        self._socket.send(buffer)
#            sent = sent + aux

    def recv(self, length):
        #received = 0
        #msg = ''
        #while received < length:
        return self._socket.recv(length)
        #msg = msg + aux
        #return msg
