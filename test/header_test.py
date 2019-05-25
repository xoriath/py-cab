import struct
import unittest

import pytest

import header, cabinet
from test_data import read_cabextract_cab, read_libmspack_cab

class TestHeader(unittest.TestCase):

    def setUp(self):
        self.cab = read_cabextract_cab('simple.cab')
        self.header = header.Header(self.cab)

    def test_signature(self):
        assert 'MSCF' == self.header.signature

    def test_size(self):
        assert 0xFD == self.header.size

    def test_file_offset(self):
        assert 0x2C == self.header.first_file_enty_offset

    def test_version(self):
        assert (1, 3) == self.header.version

    def test_number_of_folders(self):
        assert 1 == self.header.number_of_folders
    
    def test_number_of_files(self):
        assert 2 == self.header.number_of_files

    def test_flags(self):
        assert 0 == self.header.header.flags

    def test_set_id(self):
        assert 0x0622 == self.header.set_id

    def test_cabinet_number(self):
        assert 0 == self.header.sequence

    def test_optional_is_empty(self):
        assert 0 == self.header.reserved_in_header
        assert 0 == self.header.reserved_in_folder
        assert 0 == self.header.reserved_in_data
        assert '' == self.header.previous_cabinet
        assert '' == self.header.previous_disk
        assert '' == self.header.next_cabinet
        assert '' == self.header.next_disk
        assert [] == self.header.reserved_data

    def test_header_size(self):
        assert 0x24 == self.header.header_size

class TestHeaderErrorConditions(unittest.TestCase):

    def test_bad_signature(self):
        f = read_libmspack_cab('bad_signature.cab')
        
        with pytest.raises(struct.error):
            cabinet.Cabinet(f)

    