import pytest

import header, folder
from test_data import read_cabextract_cab, read_cabextract_bugs_cab

def get_folders(cab):
    h = header.Header(cab)
    return list(folder.create_folders(h, cab))

@pytest.fixture
def simple_folders():
    cab = read_cabextract_cab('simple.cab')
    return get_folders(cab)

@pytest.fixture
def lzx_folders():
    cab = read_cabextract_bugs_cab('lzx-premature-matches.cab')
    return get_folders(cab)

@pytest.fixture
def quantum_folders():
    cab = read_cabextract_bugs_cab('qtm-max-size-block.cab')
    return get_folders(cab)

def test_found_folders(simple_folders):
    assert 1 == len(simple_folders)

def test_none_compression_folder(simple_folders):
    assert folder.Compression.NONE == simple_folders[0].compression

def test_quantum_compression_folder(quantum_folders):
    assert folder.Compression.QUANTUM == quantum_folders[0].compression

def test_lzx_compression_folder(lzx_folders):
    assert folder.Compression.LZX == lzx_folders[0].compression

def test_number_of_data_entries(simple_folders):
    assert 1 == simple_folders[0].number_of_data_entries

def test_data_entry_offset(simple_folders):
    assert 0x5E == simple_folders[0].first_data_entry_offset

def test_segfault_folders():
    cab = read_cabextract_bugs_cab('cve-2014-9732-folders-segfault.cab')
    with pytest.raises(folder.UnknownFolderCompressionException):
        return get_folders(cab)