from .protocol import Protocol


class ClientProtocol(Protocol):

    def __init__(self):
        super(ClientProtocol, self).__init__()

    def send_bet(self, socket, bet):
        super()._send_byte(socket, super().BET_CHAR)
        super()._send_string(socket, bet.better_name)
        super()._send_string(socket, bet.better_last_name)
        super()._send_n_byte_number(socket, super().FOUR_BYTES, bet.better_id)
        super()._send_date(socket, bet.better_birth_date)
        super()._send_n_byte_number(socket, super().FOUR_BYTES, bet.bet_number)

    def recv_ok(self, socket):
        super()._recv_byte(socket)
