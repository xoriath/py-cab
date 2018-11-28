
import collections
import logging
import struct

class Data:
    """Each CFDATA record describes some amount of compressed data. 
    
    The first CFDATA entry for each folder is located using CFFOLDER.coffCabStart. Subsequent 
    CFDATA records for this folder are contiguous. In a standard cabinet all the CFDATA entries 
    are contiguous and in the same order as the CFFOLDER entries that refer them.
    """

    data_tuple = collections.namedtuple('CabDataHeader', 'csum cbData cbUncomp')
    data_format = '<I2H'

    def __init__(self, buffer, offset, reserved_size):
        self.header = Data.data_tuple._make(struct.unpack_from(Data.data_format, buffer=buffer, offset=offset))

        reserved_start = offset + struct.calcsize(Data.data_format)
        reserved_end = reserved_start + reserved_size
        data_start = reserved_end
        data_end = data_start + self.raw_size

        self.reserved = buffer[reserved_start : reserved_end]
        self.raw_data = buffer[data_start : data_end]

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('Parsed data: %s', self.__repr__())

    def __repr__(self):
        return '<Data checksum={cheksum} compressed={raw_size} uncompressed={uncompressed_size}>'.format(cheksum=self.checksum,
                                                                                                         raw_size=self.raw_size,
                                                                                                         uncompressed_size=self.uncompressed_size)

    @property 
    def raw_size(self):
        return self.header.cbData

    @property
    def checksum(self):
        return self.header.csum

    @property
    def uncompressed_size(self):
        return self.header.cbUncomp

    @property
    def size(self):
        return struct.calcsize(Data.data_format) + len(self.reserved) + len(self.raw_data)


def create_datas(header, folder, buffer):
    offset = folder.first_data_entry_offset
    number_of_data = folder.number_of_data_entries
    reserved_size = header.reserved_in_data

    for _ in range(number_of_data):
        data = Data(buffer, offset, reserved_size)
        offset += data.size
        yield data
