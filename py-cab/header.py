
import collections
import struct

class Header:
    """The CFHEADER structure provides information about this cabinet file.
    """

    header_tuple = collections.namedtuple('CabHeaderTuple', 'signature0 signature1 signature2 signature3 cbCabinet coffFiles version_minor version_major cFolders cFiles flags setId iCabinet')

    header_format = '<4c4xI4xI4x2B5H'
    optional_reserved_fields_format = '<H2B'

    MAX_STRING_LENGTH = 255

    # Flag values
    cfhdrPREV_CABINET = 0x0001
    cfhdrNEXT_CABINET = 0x0002
    cfhdrRESERVE_PRESENT = 0x0004

    def __init__(self, buffer):
        self.header = Header.header_tuple._make(struct.unpack_from(Header.header_format, buffer=buffer, offset=0))
       
        self._read_reserved_fields(buffer)
        self._read_reserved_data(buffer)
        self._read_previous_info(buffer)
        self._read_next_info(buffer)


    def __repr__(self):
        return self.header.__repr__()

    @property
    def signature(self):
        signature = [self.header.signature0, self.header.signature1, self.header.signature2, self.header.signature3]
        return ''.join([str(s, encoding='ascii') for s in signature])

    @property
    def size(self):
        return self.header.cbCabinet

    @property
    def first_file_enty_offset(self):   
        return self.header.coffFiles

    @property 
    def version(self):
        return (self.header.version_major, self.header.version_minor)

    @property
    def number_of_folders(self):
        return self.header.cFolders

    @property
    def number_of_files(self):
        return self.header.cFiles

    @property
    def set_id(self):
        return self.header.setId

    @property
    def sequence(self):
        return self.header.iCabinet

    @property
    def has_previous_cabinet(self):
        return self.header.flags & Header.cfhdrPREV_CABINET != 0

    @property
    def has_next_cabinet(self):
        return self.header.flags & Header.cfhdrNEXT_CABINET != 0

    @property
    def has_reserved_fields(self):
        return self.header.flags & Header.cfhdrRESERVE_PRESENT != 0

    def _read_reserved_fields(self, buffer):
        if self.has_reserved_fields:
            (self.reserved_in_header, self.reserved_in_folder, self.reserved_in_data) = \
                struct.unpack_from(Header.optional_reserved_fields_format, buffer=buffer, offset=struct.calcsize(Header.header_format))
        else:
            self.reserved_in_header = 0
            self.reserved_in_folder = 0
            self.reserved_in_data = 0

    def _read_reserved_data(self, buffer):
        if self.has_reserved_fields:
            offset = struct.calcsize(Header.header_format) + struct.calcsize(Header.optional_reserved_fields_format)
            size = self.reserved_in_header

            self.reserved_data = buffer[offset : offset + size]
        else:
            self.reserved_data = []

    def _read_previous_info(self, buffer):
        if self.has_previous_cabinet:
            offset = struct.calcsize(Header.header_format)
            if self.has_reserved_fields:
                offset += struct.calcsize(Header.optional_reserved_fields_format) + self.reserved_in_header

            strings = buffer[offset : offset + Header.MAX_STRING_LENGTH].split(b'\x00')
            self.previous_cabinet = strings[0]
            self.previous_disk = strings[1]
        else:
            self.previous_cabinet = []
            self.previous_disk = []

    def _read_next_info(self, buffer):
        if self.has_next_cabinet:
            offset = struct.calcsize(Header.header_format)
            if self.has_reserved_fields:
                offset += struct.calcsize(Header.optional_reserved_fields_format) + self.reserved_in_header

            strings = buffer[offset : offset + Header.MAX_STRING_LENGTH].split(b'\x00')
            if not self.has_previous_cabinet:
                self.next_cabinet = strings[0]
                self.next_disk = strings[1]
            else:
                self.next_cabinet = strings[2]
                self.next_disk = strings[3]
        else:
            self.next_cabinet = []
            self.next_disk = []

    @property
    def header_size(self):
        size = struct.calcsize(Header.header_format)
        if self.has_reserved_fields:
            size += struct.calcsize(Header.optional_reserved_fields_format)
        if self.reserved_data:
            size += len(self.reserved_data)
        if self.previous_cabinet:
            size += len(self.previous_cabinet) + 1
        if self.previous_disk:
            size += len(self.previous_disk) + 1
        if self.next_cabinet:
            size += len(self.next_cabinet) + 1
        if self.next_disk:
            size += len(self.next_disk) + 1

        return size



    @staticmethod
    def create(buffer):
        return Header(buffer)
    
