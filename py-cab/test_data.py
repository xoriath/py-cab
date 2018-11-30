
import os.path

CABEXTRACT_TEST_DIR = os.path.join(os.path.dirname(__file__), 'test-data', 'cabextract', 'cabs')
CABEXTRACT_BUGS_DIR = os.path.join(os.path.dirname(__file__), 'test-data', 'cabextract', 'bugs')
LIBMSPACK_TEST_DIR = os.path.join(os.path.dirname(__file__), 'test-data', 'libmspack')


def read_cabextract_cab(file_name):
        return read_cab(CABEXTRACT_TEST_DIR, file_name)

def read_cabextract_bugs_cab(file_name):
        return read_cab(CABEXTRACT_BUGS_DIR, file_name)

def read_libmspack_cab(file_name):
        return read_cab(LIBMSPACK_TEST_DIR, file_name)

def read_cab(directory, file_name):
    with open(os.path.join(directory, file_name), 'rb') as f:
        return f.read()

def read_cabextract_cases(file_name, encoding='utf-8'):
    with open(os.path.join(CABEXTRACT_TEST_DIR, file_name), 'r', encoding=encoding, errors='replace') as f:
        return [line.rstrip() for line in f.readlines() if not line.startswith('#') and line.strip()]


