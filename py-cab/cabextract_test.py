import unittest
import os.path

import cabinet
import data
import header
import folder
import file
from test_data import read_cabextract_cab, read_cabextract_cases



class CabExtractTests(unittest.TestCase):

    def test_encodings(self):
        test_cases = [
            {'cab': 'case-ascii.cab', 'cases': 'case-ascii.txt'},
            {'cab': 'case-utf8.cab', 'cases': 'case-utf8.txt'},
            {'cab': 'encoding-koi8.cab', 'cases': 'encoding-koi8.txt', 'encoding': 'koi8-r'},
            {'cab': 'encoding-latin1.cab', 'cases': 'encoding-latin1.txt', 'encoding': 'latin1'},
            {'cab': 'encoding-sjis.cab', 'cases': 'encoding-sjis.txt', 'encoding': 'shift_jisx0213'}
        ]

        for test_case in test_cases:
            cab = test_case.get('cab')
            cases = test_case.get('cases')
            encoding = test_case.get('encoding', 'utf-8')

            buffer = read_cabextract_cab(cab)
            cases = read_cabextract_cases(cases, encoding=encoding)
            
            h = header.create(buffer)
            files = list(file.create_files(h, buffer, encoding=encoding))

            self.assertHeaderAndFiles(h, files, cases)

    def test_mixed(self):
        buffer = read_cabextract_cab('split-4.cab')
        
        cab = cabinet.Cabinet(buffer)



        import pdb; pdb.set_trace()

    def assertHeaderAndFiles(self, h, files, cases):
        self.assertEqual(1, h.number_of_folders)
        self.assertEqual(len(cases), h.number_of_files)

        for (f, case) in zip(files, cases):
            self.assertEqual(case, f.name)

