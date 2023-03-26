from .protocol import Protocol


class ClientProtocol(Protocol):

    def __init__(self):
        super(ClientProtocol, self).__init__()

    def send_bet(self, socket, name, last_name, id, birth, bet_number):
        super()._send_byte(socket, super().BET_CHAR)
        super()._send_string(socket, name)
        super()._send_string(socket, last_name)
        super()._send_n_byte_number(socket, super().FOUR_BYTES, id)
        super()._send_date(socket, birth)
        super()._send_n_byte_number(socket, super().FOUR_BYTES, bet_number)

    def recv_ok(self, socket):
        super()._recv_byte(socket)
