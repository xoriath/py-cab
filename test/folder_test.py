import pytest

import header, folder
from test_data import read_cabextract_cab

@pytest.fixture
def simple_folders():
    cab = read_cabextract_cab('simple.cab')
    h = header.Header(cab)
    return list(folder.create_folders(h, cab))

def test_found_folders(simple_folders):
    assert 1 == len(simple_folders)

def test_compression(simple_folders):
    assert folder.Compression.NONE == simple_folders[0].compression

def test_number_of_data_entries(simple_folders):
    assert 1 == simple_folders[0].number_of_data_entries

def test_data_entry_offset(simple_folders):
    assert 0x5E == simple_folders[0].first_data_entry_offset
