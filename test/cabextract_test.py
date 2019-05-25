
import unittest
import os.path

import cabinet, data, header, folder, cabfile
from test_data import read_cabextract_cab, read_cabextract_cases, CABEXTRACT_TEST_DIR



class CabExtractTests(unittest.TestCase):

    def test_encodings(self):
        test_cases = [
            {'cab': 'case-ascii.cab', 'cases': 'case-ascii.txt'},
            {'cab': 'case-utf8.cab', 'cases': 'case-utf8.txt'},
            {'cab': 'encoding-koi8.cab', 'cases': 'encoding-koi8.txt', 'encoding': 'koi8-r'},
            {'cab': 'encoding-latin1.cab', 'cases': 'encoding-latin1.txt', 'encoding': 'latin1'},
            {'cab': 'encoding-sjis.cab', 'cases': 'encoding-sjis.txt', 'encoding': 'shift_jisx0213'},
            {'cab': 'utf8-stresstest.cab', 'cases': 'utf8-stresstest.txt', 'encoding': 'utf-8'}
        ]

        for test_case in test_cases:
            cab = test_case.get('cab')
            cases = test_case.get('cases')
            encoding = test_case.get('encoding', 'utf-8')

            buffer = read_cabextract_cab(cab)
            cabextract_cases = read_cabextract_cases(cases, encoding=encoding)
            
            h = header.create(buffer)
            files = list(cabfile.create_files(h, buffer, encoding=encoding))

            self.assertHeaderAndFiles(cab, h, files, cabextract_cases)

    def _mixed(self):
        split4 = os.path.join(CABEXTRACT_TEST_DIR, 'split-4.cab')
        buffer = cabinet.open_cab(split4)
        import pdb; pdb.set_trace()

    def assertHeaderAndFiles(self, cab, h, files, cases):
        assert 1 == h.number_of_folders, 'Wrong number of folders in {}'.format(cab)
        assert len(cases) == h.number_of_files, 'Wrong number of files in {}'.format(cab)

        for (f, case) in zip(files, cases):
            assert case == f.name, '[{cab}] Error in case: \n{case} != \n{name}'.format(
                                            cab=cab, 
                                            case=":".join(c.encode().hex() for c in case), 
                                            name=":".join(c.encode().hex() for c in f.name))
