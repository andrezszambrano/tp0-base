import logging
from .protocol import Protocol
from .bet import Bet

class ServerProtocol(Protocol):

    def __init__(self):
        super(ServerProtocol, self).__init__()

    def recv_bet(self, socket):
        agency = super()._recv_n_byte_number(socket, super().ONE_BYTE)
        name = super()._recv_string(socket)
        last_name = super()._recv_string(socket)
        id = super()._recv_n_byte_number(socket, super().FOUR_BYTES)
        birth_date = super()._recv_date(socket)
        bet_number = super()._recv_n_byte_number(socket, super().FOUR_BYTES)
        return Bet(agency, name, last_name, id, birth_date, bet_number)

    def recv_bets_batch(self, socket):
        bets = []
        while True:
            action_char = super()._recv_byte(socket)
            if action_char == super().BATCH_SENT:
                break
            bets.append(self.recv_bet(socket))
        return bets

    def send_ok(self, socket):
        super()._send_byte(socket, super().OK_CHAR)
