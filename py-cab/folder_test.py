import unittest

import header
import folder

from test_data import read_cabextract_cab

# From https://msdn.microsoft.com/en-us/library/bb417343.aspx#sample_cab
TEST_CAB = read_cabextract_cab('simple.cab')

class TestFolder(unittest.TestCase):

    def setUp(self):
        self.header = header.Header(TEST_CAB)
        self.folders = list(folder.create_folders(self.header, TEST_CAB))

    def test_found_folders(self):
        self.assertEqual(1, len(self.folders))

    def test_compression(self):
        self.assertEqual(folder.Compression.NONE, self.folders[0].compression)

    def test_number_of_data_entries(self):
        self.assertEqual(1, self.folders[0].number_of_data_entries)

    def test_data_entry_offset(self):
        self.assertEqual(0x5E, self.folders[0].first_data_entry_offset)
