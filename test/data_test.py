import datetime
import os

import pytest

import header, folder, data, cabinet
from test_data import read_cabextract_cab, read_libmspack_cab, CABEXTRACT_TEST_DIR

@pytest.fixture
def simple_data():
    cab = read_cabextract_cab('simple.cab')
    raw_data_block = cab[0x66:]

    h = header.Header(cab)
    folders = list(folder.create_folders(h, cab))
    f = folders[0]
    datas = list(data.create_datas(h, f, cab))

    return datas, raw_data_block

def test_data_block(simple_data):
    datas = simple_data[0]
    raw_data_block = simple_data[1]

    assert 1 == len(datas)
    
    data = datas[0]
    assert 0x30A65ABD == data.checksum
    assert 0x97 == data.raw_size
    assert 0x97 == data.uncompressed_size
    assert 0 == len(data.reserved)
    assert 0x97 == len(data.raw_data)
    assert data.valid_checksum()
    assert raw_data_block == data.raw_data

@pytest.fixture
def mixed_cab():
    return cabinet.open_cab(os.path.join(CABEXTRACT_TEST_DIR, 'mixed.cab'))

@pytest.fixture
def expected_quantum_content():
    return b'If you can read this, the Quantum decompressor is working!\n'

@pytest.fixture
def expected_mszip_content():
    return b'If you can read this, the MSZIP decompressor is working!\n'

@pytest.fixture
def expected_lzx_content():
    return b'-----------------------------------------------------------------\n' \
           b'If you can read this, the LZX decompressor is working!\n' \
           b'-----------------------------------------------------------------\n'


def test_mszip_compression(mixed_cab, expected_mszip_content):
    
    mszip_files = list(filter(lambda x: x.name == 'mszip.txt', mixed_cab.files))
    assert 1 == len(mszip_files)

    mszip_file = mszip_files[0]

    mszip_folders = list(filter(lambda x: x.index == mszip_file.folder_index, mixed_cab.folders))
    assert 1 == len(mszip_folders)

    mszip_folder = mszip_folders[0]
    assert folder.Compression.MSZIP == mszip_folder.compression
    assert 1 == mszip_folder.number_of_data_entries

    datas = list(data.create_datas(mixed_cab.header, mszip_folder, mixed_cab.buffer))
    assert 1 == len(datas)
    data_entry = datas[0]

    assert data_entry.valid_checksum()

    uncompressed_data = data_entry.data()
    assert mszip_file.file_size == len(uncompressed_data)
    assert expected_mszip_content == uncompressed_data

def test_cve_2010_2800_mszip_infinite_loop():
    f = read_libmspack_cab('cve-2010-2800-mszip-infinite-loop.cab')
    cab = cabinet.Cabinet(f)

    entries = cab.folder_and_datas[0]
    data_blocks = entries[2]

    with pytest.raises(data.InvalidChecksum):
        data_blocks[0].data()

def test_cve_2015_4470_mszip_over_read():
    f = read_libmspack_cab('cve-2015-4470-mszip-over-read.cab')
    cab = cabinet.Cabinet(f)

    entries = cab.folder_and_datas[0]
    data_blocks = entries[2]

    with pytest.raises(data.InvalidChecksum):
        data_blocks[0].data()

       

@pytest.fixture
def large_files_cab():
    return cabinet.open_cab(os.path.join(CABEXTRACT_TEST_DIR, 'large-files-cab.cab'))

@pytest.mark.skip(reason='Need to unwrap this cab twice')
def test_mszip_compression(large_files_cab):
    mszip_files = list(filter(lambda x: x.name == 'mszip-2gb.txt', large_files_cab.files))
    assert 1 == len(mszip_files)

    mszip_file = mszip_files[0]

    mszip_folders = list(filter(lambda x: x.index == mszip_file.folder_index, large_files_cab.folders))
    assert 1 == len(mszip_folders)

    mszip_folder = mszip_folders[0]
    assert cab.folder.Compression.MSZIP == mszip_folder.compression
    assert 1 == mszip_folder.number_of_data_entries

    datas = list(cab.data.create_datas(large_files_cab.header, mszip_folder, large_files_cab.buffer))
    assert 1 == len(datas)
    data_entry = datas[0]

    assert data_entry.valid_checksum()

    uncompressed_data = data_entry.data()
    assert mszip_file.file_size == len(uncompressed_data)

