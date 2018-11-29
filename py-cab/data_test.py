import unittest

import header
import folder
import data

from test_data import read_cabextract_cab

# From https://msdn.microsoft.com/en-us/library/bb417343.aspx#sample_cab
TEST_CAB = read_cabextract_cab('simple.cab')

RAW_DATA_BLOCK = TEST_CAB[0x66:]

class TestData(unittest.TestCase):

    def setUp(self):
        self.header = header.Header(TEST_CAB)
        self.folders = list(folder.create_folders(self.header, TEST_CAB))
        self.folder = self.folders[0]
        self.datas = list(data.create_datas(self.header, self.folder, TEST_CAB))

    def test_data_block(self):
        self.assertEqual(1, len(self.datas))
        
        data = self.datas[0]
        self.assertEqual(0x30A65ABD, data.checksum)
        self.assertEqual(0x97, data.raw_size)
        self.assertEqual(0x97, data.uncompressed_size)
        self.assertEqual(0, len(data.reserved))
        self.assertEqual(0x97, len(data.raw_data))
        self.assertTrue(data.valid())
        self.assertSequenceEqual(RAW_DATA_BLOCK, data.raw_data)
