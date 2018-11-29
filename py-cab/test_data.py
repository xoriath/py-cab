
import os.path

CABEXTRACT_TEST_DIR = os.path.join(os.path.dirname(__file__), 'test-data', 'cabextract', 'cabs')


def read_cabextract_cab(file_name):
    with open(os.path.join(CABEXTRACT_TEST_DIR, file_name), 'rb') as f:
        return f.read()

def read_cabextract_cases(file_name, encoding='utf-8'):
    with open(os.path.join(CABEXTRACT_TEST_DIR, file_name), 'r', encoding=encoding, errors='replace') as f:
        return [line.rstrip() for line in f.readlines() if not line.startswith('#') and line.strip()]

