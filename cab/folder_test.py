import unittest

from cab import header, folder
from cab.test_data import read_cabextract_cab

class TestFolder(unittest.TestCase):

    def setUp(self):
        self.cab = read_cabextract_cab('simple.cab')
        self.header = header.Header(self.cab)
        self.folders = list(folder.create_folders(self.header, self.cab))

    def test_found_folders(self):
        self.assertEqual(1, len(self.folders))

    def test_compression(self):
        self.assertEqual(folder.Compression.NONE, self.folders[0].compression)

    def test_number_of_data_entries(self):
        self.assertEqual(1, self.folders[0].number_of_data_entries)

    def test_data_entry_offset(self):
        self.assertEqual(0x5E, self.folders[0].first_data_entry_offset)
