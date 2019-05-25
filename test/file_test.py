import datetime
import pytest

import header, cabfile
from test_data import read_cabextract_cab

@pytest.fixture
def simple_files():
    cab = read_cabextract_cab('simple.cab')
    h = header.Header(cab)
    return list(cabfile.create_files(h, cab))

def test_found_files(simple_files):
    assert 2 == len(simple_files)

def test_hello_c(simple_files):
    hello_c = list(filter(lambda x: x.name == 'hello.c', simple_files))[0]
    
    assert (1997, 3, 12) == hello_c.date
    assert (11, 13, 52) == hello_c.time
    assert datetime.datetime(year=1997, month=3, day=12, hour=11, minute=13, second=52) == hello_c.datetime
    
    assert 0x4D == hello_c.file_size
    assert 0 == hello_c.offset_of_file_in_folder
    assert 0 == hello_c.folder_index
    assert 0x20 == hello_c.header.attribs
    assert hello_c.is_modified_since_last_backup
    
def test_welcome_c(simple_files):
    welcome_c = list(filter(lambda x: x.name == 'welcome.c', simple_files))[0]

    assert (1997, 3, 12) == welcome_c.date
    assert (11, 15, 14) == welcome_c.time
    assert datetime.datetime(year=1997, month=3, day=12, hour=11, minute=15, second=14) == welcome_c.datetime

    assert 0x4A == welcome_c.file_size
    assert 0x4D == welcome_c.offset_of_file_in_folder
    assert 0 == welcome_c.folder_index
    assert 0x20 == welcome_c.header.attribs
    assert welcome_c.is_modified_since_last_backup

