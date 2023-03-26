import datetime


class Protocol:
    OK_CHAR = 'O'
    BET_CHAR = 'B'
    FOUR_BYTES = 4
    ONE_BYTE = 1

    def __init__(self):
        pass

    def _send_byte(self, socket, char):
        socket.send(char.encode('utf-8'), self.ONE_BYTE)

    def _send_string(self, socket, string):
        str_bytes = string.encode('utf-8')
        self._send_n_byte_number(socket, 1, len(str_bytes))
        socket.send(str_bytes, len(str_bytes))

    def _send_n_byte_number(self, socket, n, number):
        BEnumber = number.to_bytes(n, byteorder='big')
        socket.send(BEnumber, n)

    def _send_date(self, socket, date):
        date_bytes = date.strftime("%Y-%m-%d").encode('utf-8')
        self._send_n_byte_number(socket, 1, len(date_bytes))
        socket.send(date_bytes, len(date_bytes))

    def _recv_byte(self, socket):
        return socket.recv(self.ONE_BYTE).decode('utf-8')

    def _recv_string(self, socket):
        str_length = self._recv_n_byte_number(socket, self.ONE_BYTE)
        return socket.recv(str_length).decode('utf-8')

    def _recv_n_byte_number(self, socket, n):
        return int.from_bytes(socket.recv(n), byteorder='big')

    def _recv_date(self, socket):
        date_len = self._recv_n_byte_number(socket, self.ONE_BYTE)
        date_str = socket.recv(date_len).decode('utf-8')
        return datetime.datetime.strptime(date_str, "%Y-%m-%d")