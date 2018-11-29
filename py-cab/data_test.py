import unittest

import header
import folder
import data

from test_data import read_cabextract_cab

class TestData(unittest.TestCase):

    def setUp(self):
        self.cab = read_cabextract_cab('simple.cab')
        self.raw_data_block = self.cab[0x66:]

        self.header = header.Header(self.cab)
        self.folders = list(folder.create_folders(self.header, self.cab))
        self.folder = self.folders[0]
        self.datas = list(data.create_datas(self.header, self.folder, self.cab))

    def test_data_block(self):
        self.assertEqual(1, len(self.datas))
        
        data = self.datas[0]
        self.assertEqual(0x30A65ABD, data.checksum)
        self.assertEqual(0x97, data.raw_size)
        self.assertEqual(0x97, data.uncompressed_size)
        self.assertEqual(0, len(data.reserved))
        self.assertEqual(0x97, len(data.raw_data))
        self.assertTrue(data.valid())
        self.assertSequenceEqual(self.raw_data_block, data.raw_data)
