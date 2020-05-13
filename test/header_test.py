import struct

import pytest

import header, cabinet, folder
from test_data import read_cabextract_cab, read_libmspack_cab

@pytest.fixture
def simple_header():
    cab = read_cabextract_cab('simple.cab')
    return header.Header(cab)

def test_signature(simple_header):
    assert 'MSCF' == simple_header.signature

def test_size(simple_header):
    assert 0xFD == simple_header.size

def test_file_offset(simple_header):
    assert 0x2C == simple_header.first_file_enty_offset

def test_version(simple_header):
    assert (1, 3) == simple_header.version

def test_number_of_folders(simple_header):
    assert 1 == simple_header.number_of_folders

def test_number_of_files(simple_header):
    assert 2 == simple_header.number_of_files

def test_flags(simple_header):
    assert 0 == simple_header.header.flags

def test_set_id(simple_header):
    assert 0x0622 == simple_header.set_id

def test_cabinet_number(simple_header):
    assert 0 == simple_header.sequence

def test_optional_is_empty(simple_header):
    assert 0 == simple_header.reserved_in_header
    assert 0 == simple_header.reserved_in_folder
    assert 0 == simple_header.reserved_in_data
    assert '' == simple_header.previous_cabinet
    assert '' == simple_header.previous_disk
    assert '' == simple_header.next_cabinet
    assert '' == simple_header.next_disk
    assert [] == simple_header.reserved_data

def test_header_size(simple_header):
    assert 0x24 == simple_header.header_size

def test_bad_signature():
    f = read_libmspack_cab('bad_signature.cab')
    
    with pytest.raises(folder.InvalidFolderHeader):
        cabinet.Cabinet(f)

