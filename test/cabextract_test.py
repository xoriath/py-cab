
import pytest
import os.path

import cabinet, data, header, folder, cabfile
from test_data import read_cabextract_cab, read_cabextract_cases, CABEXTRACT_TEST_DIR

@pytest.mark.parametrize("cab, cases, encoding", [
        ('case-ascii.cab', 'case-ascii.txt', 'utf-8'),
        ('case-utf8.cab', 'case-utf8.txt', 'utf-8'),
        ('encoding-koi8.cab', 'encoding-koi8.txt', 'koi8-r'),
        ('encoding-latin1.cab', 'encoding-latin1.txt', 'latin1'),
        ('encoding-sjis.cab', 'encoding-sjis.txt', 'shift_jisx0213'),
        ('utf8-stresstest.cab', 'utf8-stresstest.txt', 'utf-8')
    ])
def test_encodings(cab, cases, encoding):

    buffer = read_cabextract_cab(cab)
    cabextract_cases = read_cabextract_cases(cases, encoding=encoding)
    
    h = header.create(buffer)
    files = list(cabfile.create_files(h, buffer, encoding=encoding))

    assertHeaderAndFiles(cab, h, files, cabextract_cases)

def _mixed():
    split4 = os.path.join(CABEXTRACT_TEST_DIR, 'split-4.cab')
    buffer = cabinet.open_cab(split4)
    import pdb; pdb.set_trace()

def assertHeaderAndFiles(cab, h, files, cases):
    assert 1 == h.number_of_folders, 'Wrong number of folders in {}'.format(cab)
    assert len(cases) == h.number_of_files, 'Wrong number of files in {}'.format(cab)

    for (f, case) in zip(files, cases):
        assert case == f.name, '[{cab}] Error in case: \n{case} != \n{name}'.format(
                                        cab=cab, 
                                        case=":".join(c.encode().hex() for c in case), 
                                        name=":".join(c.encode().hex() for c in f.name))

