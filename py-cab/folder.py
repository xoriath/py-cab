
import collections
import struct

class Folder:
    """Each CFFOLDER structure contains information about one of the folders or partial folders stored in this cabinet file. 
    The first CFFOLDER entry immediately follows the CFHEADER entry and subsequent CFFOLDER records for this cabinet are contiguous. 
    CFHEADER.cFolders indicates how many CFFOLDER entries are present.

    Folders may start in one cabinet, and continue on to one or more succeeding cabinets. When the cabinet file creator 
    detects that a folder has been continued into another cabinet, it will complete that folder as soon as the current 
    file has been completely compressed. Any additional files will be placed in the next folder. Generally, this means 
    that a folder would span at most two cabinets, but if the file is large enough, it could span more than two cabinets.

    CFFOLDER entries actually refer to folder fragments, not necessarily complete folders. A CFFOLDER structure is the 
    beginning of a folder if the iFolder value in the first file referencing the folder does not indicate the folder is 
    continued from the previous cabinet file.

    The typeCompress field may vary from one folder to the next, unless the folder is continued from a previous cabinet file.
    """

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
        