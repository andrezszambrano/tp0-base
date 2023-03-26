from .protocol import Protocol


class ClientProtocol(Protocol):

    def __init__(self):
        super(ClientProtocol, self).__init__()

    def send_bet(self, socket, bet):
        super()._send_byte(socket, super().BET_CHAR)
        super()._send_n_byte_number(socket, super().ONE_BYTE, bet.agency)
        super()._send_string(socket, bet.first_name)
        super()._send_string(socket, bet.last_name)
        super()._send_n_byte_number(socket, super().FOUR_BYTES, bet.document)
        super()._send_date(socket, bet.birthdate)
        super()._send_n_byte_number(socket, super().FOUR_BYTES, bet.number)

    def recv_ok(self, socket):
        super()._recv_byte(socket)
