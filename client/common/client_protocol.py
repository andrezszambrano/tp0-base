from .protocol import Protocol


class ClientProtocol(Protocol):

    def __init__(self):
        super(ClientProtocol, self).__init__()

    def __send_bet(self, socket, bet):
        super()._send_byte(socket, super().BET_CHAR)
        super()._send_string(socket, bet.first_name)
        super()._send_string(socket, bet.last_name)
        super()._send_n_byte_number(socket, super().FOUR_BYTES, bet.document)
        super()._send_date(socket, bet.birthdate)
        super()._send_n_byte_number(socket, super().FOUR_BYTES, bet.number)

    def send_batch(self, socket, batch):
        super()._send_byte(socket, super().START_BATCH)
        for bet in batch:
            self.__send_bet(socket, bet)
        super()._send_byte(socket, super().BATCH_SENT)

    def send_agency_number(self, socket, agency_number):
        super()._send_n_byte_number(socket, super().ONE_BYTE, agency_number)

    def send_finished_message(self, socket):
        super()._send_byte(socket, super().FINISHED_CHAR)

    def try_to_recv_winners_documents(self, socket):
        super()._send_byte(socket, super().CONSULT_WINNERS)
        action = super()._recv_byte(socket)
        if action != super().OK_CHAR:
            return None
        return self.__recv_winners_documents(socket)

    def __recv_winners_documents(self, socket):
        winners = []
        while True:
            action = super()._recv_byte(socket)
            if action == super().FINISHED_CHAR:
                break
            winners.append(super()._recv_n_byte_number(socket, super().FOUR_BYTES))
        return winners

    def recv_ok(self, socket):
        super()._recv_byte(socket)
