import datetime
import os
import unittest

import header
import folder
import data
import cabinet

from test_data import read_cabextract_cab, read_libmspack_cab, CABEXTRACT_TEST_DIR

class TestSimpleData(unittest.TestCase):

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
        self.assertTrue(data.valid_checksum())
        self.assertSequenceEqual(self.raw_data_block, data.raw_data)

class TestCompressedData(unittest.TestCase):
    def setUp(self):
        self.cab = cabinet.open_cab(os.path.join(CABEXTRACT_TEST_DIR, 'mixed.cab'))
        
        self.expected_quantum_content = b'If you can read this, the Quantum decompressor is working!\n'
        self.expected_mszip_content = b'If you can read this, the MSZIP decompressor is working!\n'
        self.expected_lzx_content = b'-----------------------------------------------------------------\n' \
                                    b'If you can read this, the LZX decompressor is working!\n' \
                                    b'-----------------------------------------------------------------\n'


    def test_mszip_compression(self):
        
        mszip_files = list(filter(lambda x: x.name == 'mszip.txt', self.cab.files))
        self.assertEqual(1, len(mszip_files))

        mszip_file = mszip_files[0]

        mszip_folders = list(filter(lambda x: x.index == mszip_file.folder_index, self.cab.folders))
        self.assertEqual(1, len(mszip_folders))

        mszip_folder = mszip_folders[0]
        self.assertEqual(folder.Compression.MSZIP, mszip_folder.compression)
        self.assertEqual(1, mszip_folder.number_of_data_entries)

        datas = list(data.create_datas(self.cab.header, mszip_folder, self.cab.buffer))
        self.assertEqual(1, len(datas))
        data_entry = datas[0]

        self.assertTrue(data_entry.valid_checksum())

        uncompressed_data = data_entry.data()
        self.assertEqual(mszip_file.file_size, len(uncompressed_data))
        self.assertEqual(self.expected_mszip_content, uncompressed_data)
    
    def test_cve_2010_2800_mszip_infinite_loop(self):
        f = read_libmspack_cab('cve-2010-2800-mszip-infinite-loop.cab')
        cab = cabinet.Cabinet(f)

        entries = cab.folder_and_datas[0]
        data_blocks = entries[2]

        with self.assertRaises(data.InvalidChecksum):
            data_blocks[0].data()

    def test_cve_2015_4470_mszip_over_read(self):
        f = read_libmspack_cab('cve-2015-4470-mszip-over-read.cab')
        cab = cabinet.Cabinet(f)

        entries = cab.folder_and_datas[0]
        data_blocks = entries[2]

        with self.assertRaises(data.InvalidChecksum):
            data_blocks[0].data()

       

class TestHugeCompressedData(): # unittest.TestCase
    def setUp(self):
        self.cab = cabinet.open_cab(os.path.join(CABEXTRACT_TEST_DIR, 'large-files-cab.cab'))

    def test_mszip_compression(self):
        mszip_files = list(filter(lambda x: x.name == 'mszip-2gb.txt', self.cab.files))
        self.assertEqual(1, len(mszip_files))

        mszip_file = mszip_files[0]

        mszip_folders = list(filter(lambda x: x.index == mszip_file.folder_index, self.cab.folders))
        self.assertEqual(1, len(mszip_folders))

        mszip_folder = mszip_folders[0]
        self.assertEqual(folder.Compression.MSZIP, mszip_folder.compression)
        self.assertEqual(1, mszip_folder.number_of_data_entries)

        datas = list(data.create_datas(self.cab.header, mszip_folder, self.cab.buffer))
        self.assertEqual(1, len(datas))
        data_entry = datas[0]

        self.assertTrue(data_entry.valid_checksum())

        uncompressed_data = data_entry.data()
        self.assertEqual(mszip_file.file_size, len(uncompressed_data))
