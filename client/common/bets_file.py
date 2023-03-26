import csv
import datetime
from .bet import Bet

class BetsFile():
    def __init__(self):
        pass

    def get_bets(self, agency_id, path):
        with open(path, 'r') as file:
            reader = csv.reader(file, quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                yield Bet(agency_id, row[0], row[1], int(row[2]),
                          datetime.date.fromisoformat(row[3]),
                          int(row[4]))
