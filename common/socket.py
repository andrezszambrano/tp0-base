import socket


class Socket:

    def __init__(self, host, port, created_socket = None):
        _socket = None
        if created_socket != None:
            _socket = created_socket
        else:
            _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            _socket.connect((host, port))
        self._socket = _socket

    def getpeername(self):
        return self._socket.getpeername()

    def get_addr(self):
        return self._socket.getsockname()[0]

    def shutdown_and_close(self):
        self._socket.shutdown(socket.SHUT_RDWR)
        self._socket.close()

    def send(self, buffer, length):
        sent = 0
        remainder = buffer
        while sent < length:
            aux = self._socket.send(remainder)
            remainder = buffer
            sent = sent + aux

    def recv(self, length):
        #received = 0
        #msg = ''
        #while received < length:
        return self._socket.recv(length)
        #msg = msg + aux
        #return msg
