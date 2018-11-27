import unittest
import os.path

import header
import folder
import file
import data

CABEXTRACT_TEST_DIR = os.path.join(os.path.dirname(__file__), 'test-data', 'cabextract', 'cabs')


class CabExtractTests(unittest.TestCase):

    def test_filenames(self):
        test_cases = [
            {'cab': 'case-ascii.cab', 'cases': 'case-ascii.txt'},
            {'cab': 'case-utf8.cab', 'cases': 'case-utf8.txt'},
            {'cab': 'encoding-koi8.cab', 'cases': 'encoding-koi8.txt', 'encoding': 'koi8-r'},
            {'cab': 'encoding-latin1.cab', 'cases': 'encoding-latin1.txt', 'encoding': 'latin1'}
        ]

        for test_case in test_cases:
            cab = test_case.get('cab')
            cases = test_case.get('cases')
            encoding = test_case.get('encoding', 'utf-8')

            buffer = read_cab(cab)
            cases = read_cases(cases, encoding=encoding)
            
            h = header.create(buffer)
            files = list(file.create_files(h, buffer, encoding=encoding))

            self.assertHeaderAndFiles(h, files, cases)

    def assertHeaderAndFiles(self, h, files, cases):
        self.assertEqual(1, h.number_of_folders)
        self.assertEqual(len(cases), h.number_of_files)

        for (f, case) in zip(files, cases):
            self.assertEqual(case, f.name)


def read_cab(file_name):
    with open(os.path.join(CABEXTRACT_TEST_DIR, file_name), 'rb') as f:
        return f.read()

def read_cases(file_name, encoding='utf-8'):
    with open(os.path.join(CABEXTRACT_TEST_DIR, file_name), 'rb') as f:
        return [line.rstrip().decode(encoding) for line in f.readlines() if not line.startswith(b'#')]

