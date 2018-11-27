
import collections
import struct

class Folder:

    folder_tuple = collections.namedtuple('CabFolderTuple', 'coffCabStart cCFData typeCompress')
    folder_format = '<I2H'

    def __init__(self, buffer, offset, reserved):
        self.header = Folder.folder_tuple._make(struct.unpack_from(Folder.folder_format, buffer=buffer, offset=offset))

        reserved_offset = offset + struct.calcsize(Folder.folder_format)
        self.reserved = buffer[reserved_offset : reserved_offset + reserved]

    @property 
    def first_data_entry_offset(self):
        return self.header.coffCabStart

    @property
    def number_of_data_entries(self):
        return self.header.cCFData

    @property
    def compression(self):
        return self.header.typeCompress

    @property
    def size(self):
        return struct.calcsize(Folder.folder_format) + len(self.reserved)


def create_folders(header, buffer):
    number_of_folders = header.number_of_folders
    offset = header.header_size
    folder_reserved = header.reserved_in_folder

    for _ in range(number_of_folders):
        folder = Folder(buffer, offset, folder_reserved)
        offset += folder.size
        yield folder
        