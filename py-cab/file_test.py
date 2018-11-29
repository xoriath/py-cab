import unittest

import header
import file

from test_data import read_cabextract_cab

class TestFile(unittest.TestCase):

    def setUp(self):
        self.cab = read_cabextract_cab('simple.cab')
        self.header = header.Header(self.cab)
        self.files = list(file.create_files(self.header, self.cab))

    def test_found_files(self):
        self.assertEqual(2, len(self.files))

    def test_hello_c(self):
        hello_c = list(filter(lambda x: x.name == 'hello.c', self.files))[0]
        
        self.assertTupleEqual((1997, 3, 12), hello_c.date)
        self.assertTupleEqual((11, 13, 52), hello_c.time)
        
        self.assertEqual(0x4D, hello_c.file_size)
        self.assertEqual(0, hello_c.offset_of_file_in_folder)
        self.assertEqual(0, hello_c.folder_index)
        self.assertEqual(0x20, hello_c.header.attribs)
        self.assertTrue(hello_c.is_modified_since_last_backup)
        
    def test_welcome_c(self):
        welcome_c = list(filter(lambda x: x.name == 'welcome.c', self.files))[0]

        self.assertTupleEqual((1997, 3, 12), welcome_c.date)
        self.assertTupleEqual((11, 15, 14), welcome_c.time)

        self.assertEqual(0x4A, welcome_c.file_size)
        self.assertEqual(0x4D, welcome_c.offset_of_file_in_folder)
        self.assertEqual(0, welcome_c.folder_index)
        self.assertEqual(0x20, welcome_c.header.attribs)
        self.assertTrue(welcome_c.is_modified_since_last_backup)

