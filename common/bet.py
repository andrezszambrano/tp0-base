import datetime


""" A lottery bet registry. """
class Bet:
    def __init__(self, agency: int, first_name: str, last_name: str, document: int,
                 birthdate: datetime.date, number: int):
        """
        agency must be passed with integer format.
        birthdate must be passed with format: 'YYYY-MM-DD'.
        number must be passed with integer format.
        """
        self.agency = agency
        self.first_name = first_name
        self.last_name = last_name
        self.document = document
        self.birthdate = birthdate
        self.number = number