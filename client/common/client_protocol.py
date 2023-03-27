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

    def send_batch(self, socket, batch):
        super()._send_byte(socket, super().START_BATCH)
        for bet in batch:
            self.send_bet(socket, bet)
        super()._send_byte(socket, super().BATCH_SENT)

    def send_finished_message(self, socket, agency_id):
        super()._send_byte(socket, super().FINISHED_CHAR)
        super()._send_n_byte_number(socket, super().ONE_BYTE, agency_id)

    def recv_number_of_winners(self, socket, agency_id):
        super()._send_byte(socket, super().CONSULT_WINNERS)
        action = super()._recv_byte(socket)
        if action != super().OK_CHAR:
            return -1
        super()._send_n_byte_number(socket, super().ONE_BYTE, agency_id)
        return super()._recv_n_byte_number(socket, super().TWO_BYTES)

    def recv_ok(self, socket):
        super()._recv_byte(socket)
