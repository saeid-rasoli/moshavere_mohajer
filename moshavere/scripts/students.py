from csv import reader
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
filename = BASE_DIR / "data/daneshjoo.csv"


def load_file(filename):
    csv_file = list()
    with open(filename, "r", errors='ignore') as f:
        csv_reader = reader(f)
        for row in csv_reader:
            if not row:
                continue
            csv_file.append(row)
    return csv_file


daneshjoo = load_file(filename)
headers = daneshjoo[0]
records = daneshjoo[1:]
