import struct
import unittest

from cab import header, cabinet
from cab.test_data import read_cabextract_cab, read_libmspack_cab

class TestHeader(unittest.TestCase):

    def setUp(self):
        self.cab = read_cabextract_cab('simple.cab')
        self.header = header.Header(self.cab)

    def test_signature(self):
        self.assertEqual('MSCF', self.header.signature)

    def test_size(self):
        self.assertEqual(0xFD, self.header.size)

    def test_file_offset(self):
        self.assertEqual(0x2C, self.header.first_file_enty_offset)

    def test_version(self):
        self.assertTupleEqual((1, 3), self.header.version)

    def test_number_of_folders(self):
        self.assertEqual(1, self.header.number_of_folders)
    
    def test_number_of_files(self):
        self.assertEqual(2, self.header.number_of_files)

    def test_flags(self):
        self.assertEqual(0, self.header.header.flags)

    def test_set_id(self):
        self.assertEqual(0x0622, self.header.set_id)

    def test_cabinet_number(self):
        self.assertEqual(0, self.header.sequence)

    def test_optional_is_empty(self):
        self.assertEqual(0, self.header.reserved_in_header)
        self.assertEqual(0, self.header.reserved_in_folder)
        self.assertEqual(0, self.header.reserved_in_data)
        self.assertEqual('', self.header.previous_cabinet)
        self.assertEqual('', self.header.previous_disk)
        self.assertEqual('', self.header.next_cabinet)
        self.assertEqual('', self.header.next_disk)
        self.assertEqual([], self.header.reserved_data)

    def test_header_size(self):
        self.assertEqual(0x24, self.header.header_size)

class TestHeaderErrorConditions(unittest.TestCase):

    def test_bad_signature(self):
        f = read_libmspack_cab('bad_signature.cab')
        
        with self.assertRaises(struct.error):
            cabinet.Cabinet(f)

    