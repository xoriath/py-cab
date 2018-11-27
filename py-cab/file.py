
import collections
import logging
import struct

class File:

    MAX_STRING_LENGTH = 255

    file_tuple = collections.namedtuple('CabFileTuple', 'cbFile uoffFolderStart iFolder date time attribs')
    file_format = '<2I4H'

    # Flags in folder index
    ifoldCONTINUED_FROM_PREV = 0xFFFD
    ifoldCONTINUED_TO_NEXT = 0xFFFE
    ifoldCONTINUED_PREV_AND_NEXT = 0xFFFF

    # Attributes
    _A_RDONLY = 0x01
    _A_HIDDEN = 0x02
    _A_SYSTEM = 0x04
    _A_ARCH = 0x20
    _A_EXEC = 0x40
    _A_NAME_IS_UTF = 0x80

    def __init__(self, buffer, offset: int):
        self.header = File.file_tuple._make(struct.unpack_from(File.file_format, buffer=buffer, offset=offset))
        self.name = self._read_file_name(buffer, offset)
        self.logger = logging.getLogger()

    def __repr__(self):
        return '<File {name}: {header}>'.format(name=self.name, header=self.header)

    def _read_file_name(self, buffer, offset: int) -> str:
        if not self.is_name_utf:
            offset += struct.calcsize(File.file_format)
            strings = buffer[offset : offset + File.MAX_STRING_LENGTH].split(b'\x00')
            return strings[0].decode('ascii')
        else:
            raise Exception("Cannot decode utf characters")

    @property
    def is_read_only(self) -> bool:
        return self.header.attribs & File._A_RDONLY != 0

    @property
    def is_hidden(self) -> bool:
        return self.header.attribs & File._A_HIDDEN != 0

    @property
    def is_system(self) -> bool:
        return self.header.attribs & File._A_SYSTEM != 0

    @property
    def is_modified_since_last_backup(self) -> bool:
        return self.header.attribs & File._A_ARCH != 0

    @property
    def run_after_extraction(self) -> bool:
        return self.header.attribs & File._A_EXEC != 0
    
    @property
    def is_name_utf(self) -> bool:
        return self.header.attribs & File._A_NAME_IS_UTF != 0

    @property 
    def file_size(self) -> int:
        return self.header.cbFile

    @property
    def offset_of_file_in_folder(self) -> int:
        return self.header.uoffFolderStart

    @property
    def folder_index(self) -> int:
        return self.header.iFolder

    @property
    def date(self):
        year = (self.header.date >> 9) + 1980
        month = (self.header.date >> 5) & 0xF
        day = self.header.date & 0x1F

        return (year, month, day)

    @property
    def time(self):
        hour = self.header.time >> 11
        minute = (self.header.time >> 5) & 0x3F
        second = (self.header.time << 1) & 0x3E

        return (hour, minute, second)

    @property
    def attributes(self):
        return self.header.attribs

    @property
    def size(self):
        return struct.calcsize(File.file_format) + len(self.name) + 1 # +1 for NULL in name string


def create_files(header, buffer):
    number_of_files = header.number_of_files
    offset = header.first_file_enty_offset

    for _ in range(number_of_files):
        file = File(buffer, offset)
        offset += file.size
        yield file
        