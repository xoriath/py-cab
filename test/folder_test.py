import unittest

import header, folder
from test_data import read_cabextract_cab

class TestFolder(unittest.TestCase):

    def setUp(self):
        self.cab = read_cabextract_cab('simple.cab')
        self.header = header.Header(self.cab)
        self.folders = list(folder.create_folders(self.header, self.cab))

    def test_found_folders(self):
        assert 1 == len(self.folders)

    def test_compression(self):
        assert folder.Compression.NONE == self.folders[0].compression

    def test_number_of_data_entries(self):
        assert 1 == self.folders[0].number_of_data_entries

    def test_data_entry_offset(self):
        assert 0x5E == self.folders[0].first_data_entry_offset
