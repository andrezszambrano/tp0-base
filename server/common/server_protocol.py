import logging
from .protocol import Protocol


class ServerProtocol(Protocol):

    def __init__(self):
        super(ServerProtocol, self).__init__()

    def recv_bet(self, socket):
        super()._recv_byte(socket)
        name = super()._recv_string(socket)
        last_name = super()._recv_string(socket)
        id = super()._recv_n_byte_number(socket, super().FOUR_BYTES)
        birth_date = super()._recv_date(socket)
        bet_number = super()._recv_n_byte_number(socket, super().FOUR_BYTES)
        logging.debug(f"name: {name}, last name: {last_name}, id: {id}, birth date: {birth_date}, bet number: {bet_number}")
        return name, last_name, id, birth_date, bet_number

    def send_ok(self, socket):
        super()._send_byte(socket, super().OK_CHAR)
